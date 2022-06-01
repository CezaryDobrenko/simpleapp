from django.http import HttpResponse
from django.utils import timezone

from scrapper.models.collected_data import CollectedData
from scrapper.models.folder import Folder
from scrapper.models.selectors import Selector
from scrapper.models.utils.intervals import Interval
from scrapper.models.website import Website

from .scrapper import Scrapper


def calculate_new_scrape_date(last_scraping: str, interval: str) -> tuple:
    now = timezone.now()
    next_scrape_date = Interval.find_next_scraping_date(last_scraping, interval)
    if next_scrape_date is None:
        is_valid = True
        new_date = now
    elif now > next_scrape_date:
        is_valid = True
        new_date = now
    else:
        is_valid = False
        new_date = None
    return is_valid, new_date


def scheduler(request, interval: str) -> HttpResponse:
    for folder in Folder.objects.filter(is_ready=True):
        try:
            is_valid, new_date = calculate_new_scrape_date(
                folder.last_scraping, folder.scraping_interval
            )
            if is_valid:
                folder.update_last_scraping(new_date)
                if websites := Website.objects.filter(
                    folder_id=folder.id, is_ready=True
                ):
                    for website in websites:
                        is_new_data_collected = False
                        if selectors := Selector.objects.filter(website_id=website.id):
                            scrapper = Scrapper(website.url)
                            for selector in selectors:
                                data = scrapper.scrape_website(
                                    selector.selector_type.name,
                                    selector.value,
                                    website.is_simplified,
                                )
                                for item in data:
                                    _, created = CollectedData.objects.get_or_create(
                                        value=item, selector=selector
                                    )
                                    if created:
                                        is_new_data_collected = True
                        if is_new_data_collected:
                            website.update_is_new_data_collected(is_new_data_collected)
        except:
            pass
    return HttpResponse("Data has been scrapped")
