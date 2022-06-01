import re

import cfscrape
import html_to_json
from bs4 import BeautifulSoup


class Scrapper:
    scrapper: object
    url: str
    selectors: list
    content: str
    soup: list

    def __init__(self, url: str, is_mocked: bool = False):
        self.scraper = cfscrape.create_scraper()
        self.url = url
        if not is_mocked:
            content = self.__download_content(url)
            self.content = content
            self.soup = BeautifulSoup(content, "html.parser")
        else:
            content = open("mocked_website.html", "r")
            self.content = content
            self.soup = BeautifulSoup(content, "html.parser")

    def __download_content(self, url) -> str:
        return self.scraper.get(url).content

    def __remove_html_tags(self, results: list, replace: str = "") -> list:
        parsed_results = []
        for result in results:
            parsed_result = re.sub(re.compile("<.*?>"), replace, str(result))
            parsed_results.append(parsed_result)
        return parsed_results

    def __parse_to_json(self, results: list) -> list:
        parsed_results = []
        for result in results:
            stringify_result = str(result)
            json_unparsed = str(html_to_json.convert(stringify_result))
            json_parsed = json_unparsed.replace("'", '"')
            parsed_results.append(json_parsed)
        return parsed_results

    def __get_custom_selectors(self, cusotm_selector: str) -> list:
        if cusotm_selector == "list":
            return ["li"]
        if cusotm_selector == "headline":
            return ["h1", "h2", "h3", "h4", "h5", "h6"]
        if cusotm_selector == "table":
            return ["th", "td"]
        return []

    def scrape_website(
        self, selector_type: str, selector_value: str, is_simplified: bool
    ) -> list:
        if selector_type == "tag":
            if selector_value in ["list", "headline", "table"]:
                selectors = self.__get_custom_selectors(selector_value)
                results = []
                for selector in selectors:
                    result = self.soup.findAll(selector)
                    results = results + result
            else:
                results = self.soup.findAll(selector_value)
        else:
            results = self.soup.find_all(True, {selector_type: selector_value})
        if is_simplified:
            parsed_results = self.__parse_to_json(results)
        else:
            parsed_results = self.__remove_html_tags(results, replace=" ")
        return parsed_results

    def get_content(self) -> str:
        return self.content

    def get_soup(self) -> str:
        return self.soup
