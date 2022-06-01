from datetime import timedelta
from typing import Optional

from django.db import models


class Interval:
    class Options(models.TextChoices):
        MINUTE5 = "MINUTE5"
        MINUTE10 = "MINUTE10"
        MINUTE15 = "MINUTE15"
        MINUTE30 = "MINUTE30"
        MINUTE45 = "MINUTE45"
        HOUR1 = "HOUR1"
        HOUR2 = "HOUR2"
        HOUR3 = "HOUR3"
        HOUR6 = "HOUR6"
        HOUR12 = "HOUR12"
        DAY1 = "DAY1"
        DAY2 = "DAY2"
        DAY3 = "DAY3"
        DAY4 = "DAY4"
        DAY5 = "DAY5"
        DAY6 = "DAY6"
        WEEK = "WEEK"

    def check_if_interval_exist(value: str) -> Optional[str]:
        intervals = {i.name: i.value for i in Interval.Options}
        if value in intervals:
            return value
        raise Exception("Non existing interval")

    def find_next_scraping_date(
        last_scrape_date: str, scrape_interval: str
    ) -> Optional[str]:
        if last_scrape_date is None:
            return last_scrape_date

        return {
            "MINUTE5": last_scrape_date + timedelta(minutes=5),
            "MINUTE10": last_scrape_date + timedelta(minutes=10),
            "MINUTE15": last_scrape_date + timedelta(minutes=15),
            "MINUTE30": last_scrape_date + timedelta(minutes=30),
            "MINUTE45": last_scrape_date + timedelta(minutes=45),
            "HOUR1": last_scrape_date + timedelta(hours=1),
            "HOUR2": last_scrape_date + timedelta(hours=2),
            "HOUR3": last_scrape_date + timedelta(hours=3),
            "HOUR6": last_scrape_date + timedelta(hours=6),
            "HOUR12": last_scrape_date + timedelta(hours=12),
            "DAY1": last_scrape_date + timedelta(days=1),
            "DAY2": last_scrape_date + timedelta(days=2),
            "DAY3": last_scrape_date + timedelta(days=3),
            "DAY4": last_scrape_date + timedelta(days=4),
            "DAY5": last_scrape_date + timedelta(days=5),
            "DAY6": last_scrape_date + timedelta(days=6),
            "WEEK": last_scrape_date + timedelta(days=7),
        }[scrape_interval]
