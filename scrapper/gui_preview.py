import cfscrape
from bs4 import BeautifulSoup


class GUIPreview:
    scraper = cfscrape.create_scraper()

    def get_preview(url):
        try:
            content = GUIPreview.scraper.get(url).content
        except:
            content = "<div>Nie udało się pobrać strony!</div>"
        soup = BeautifulSoup(content, "html.parser")
        parsed_soup = GUIPreview.parse_soup(soup)
        return parsed_soup

    def get_mocked_preview(self):
        content = """
            <html>
                <head>
                    <script>
                        console.log(1);
                    </script>
                    <style>
                        body{
                            border: solid 1px black;
                        }
                    </style>
                </head>
                <body>
                    <a href="www.google.pl">Link to google!</a>
                    Nice website :)
                </body>
            </html>
        """
        soup = BeautifulSoup(content, "html.parser")
        parsed_soup = GUIPreview.parse_soup(soup)
        return parsed_soup

    def parse_soup(soup):
        unwanted_tags = ["script", "style", "link", "head", "svg"]
        unwanted_elements = [("a", "href"), (None, "style")]
        for tag in unwanted_tags:
            soup = GUIPreview._extract_unwanted_item(soup, tag)
        for element in unwanted_elements:
            marker, attribute = element
            soup = GUIPreview._delete_unwanted_attribute(soup, marker, attribute)
        soup = GUIPreview._add_attribute_to_element(
            soup, "img", "style", "max-height: 40%; max-width: 40%;"
        )
        return soup

    def _extract_unwanted_item(soup, item_type):
        for s in soup.select(item_type):
            s.extract()
        return soup

    def _delete_unwanted_attribute(soup, marker, attribute):
        for s in soup.find_all(marker):
            del s[attribute]
        return soup

    def _add_attribute_to_element(soup, marker, attribute, value):
        for s in soup.find_all(marker):
            s[attribute] = value
        return soup
