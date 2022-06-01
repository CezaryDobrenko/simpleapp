from django.test import TestCase
from scheduler.scrapper import Scrapper
from scheduler.views import calculate_new_scrape_date


class ScrapperTests(TestCase):
    def test_scrapper_simplified_preview(self):
        scrapper = Scrapper(url="www.test.pl", is_mocked=True)
        data = scrapper.scrape_website(
            "class", "number-boxes-itemm-number", is_simplified=False
        )
        expected = [
            " +48727801958 ",
            " +48727801893 ",
            " +48722717428 ",
            " +16466623058 ",
            " +16466787403 ",
            " +16465106465 ",
            " +34681999929 ",
            " +34681993330 ",
            " +34681991234 ",
            " +380999373708 ",
            " +4915227654357 ",
            " +447399819350 ",
            " +380934611643 ",
            " +380999134159 ",
            " +447548032829 ",
            " +447548032890 ",
            " +447950636683 ",
            " +447399819347 ",
            " +447950640748 ",
            " +447944649105 ",
            " +447548032916 ",
            " +447716535176 ",
            " +447548032886 ",
            " +447933447754 ",
            " +447533398730 ",
            " +447548032994 ",
            " +447767916441 ",
            " +4915207955279 ",
            " +4915207930698 ",
            " +4915227654381 ",
            " +4915207829731 ",
            " +4915207829969 ",
            " +972552992022 ",
            " +972552992023 ",
            " +972552603210 ",
            " +16465089359 ",
            " +33752124546 ",
            " +420721482610 ",
            " +420721482480 ",
            " +31645402591 ",
            " +31613355460 ",
            " +918527834283 ",
            " +917428731210 ",
            " +917428723247 ",
            " +917428730930 ",
            " +917428730894 ",
            " +77789490686 ",
            " +77789490683 ",
            " +905347601441 ",
            " +447904694150 ",
            " +559551583801 ",
            " +353894060424 ",
            " +447923590965 ",
            " +447599143079 ",
            " +447842646591 ",
            " +447591156667 ",
            " +447938562268 ",
            " +447944633730 ",
            " +447508629557 ",
            " +447903612563 ",
            " +447940406246 ",
            " +447376493559 ",
            " +447399305426 ",
            " +447398668365 ",
            " +447399533453 ",
            " +447376494399 ",
            " +447398668366 ",
            " +351910602986 ",
            " +528184713166 ",
            " +6281905017120 ",
            " +6281905013973 ",
            " +447533403149 ",
            " +2348153353131 ",
        ]
        assert data == expected

    def test_scrapper_not_simplified_preview(self):
        scrapper = Scrapper(url="www.test.pl", is_mocked=True)
        data = scrapper.scrape_website(
            "class", "number-boxes-item-country", is_simplified=True
        )
        expected = [
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Poland"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Poland"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Poland"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United States"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United States"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United States"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Spain"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Spain"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Spain"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Ukraine"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Ukraine"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Ukraine"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Germany"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Israel"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Israel"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Israel"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Canada"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "France"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Czech Republic"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Czech Republic"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Netherlands"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Netherlands"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "India"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "India"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "India"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "India"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "India"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Kazakhstan"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Kazakhstan"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Turkey"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Brazil"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Ireland"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Portugal"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Mexico"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Indonesia"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Indonesia"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "United Kingdom"}]}',
            '{"h5": [{"_attributes": {"class": ["number-boxes-item-country", "number-boxess-item-country"]}, "_value": "Nigeria"}]}',
        ]
        assert data == expected

    def test_scrapper_get_content(self):
        scrapper = Scrapper(url="www.test.pl", is_mocked=True)
        content = scrapper.get_content()
        assert content is not None

    def test_scrapper_get_soup(self):
        scrapper = Scrapper(url="www.test.pl", is_mocked=True)
        content = scrapper.get_soup()
        assert content is not None

    def test_calculate_new_scrape_date(self):
        assert calculate_new_scrape_date(None, "Hour1")
