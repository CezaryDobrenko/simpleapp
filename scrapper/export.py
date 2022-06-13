import json
from json import loads

from dicttoxml import dicttoxml

from scrapper.models.collected_data import CollectedData
from scrapper.models.selectors import Selector
from scrapper.models.website import Website


class Export:
    def __init__(self, folder_id: int):
        self.folder_id = folder_id

    def export_as_txt(self) -> str:
        output = ""
        for website in Website.objects.filter(folder_id=self.folder_id, is_ready=True):
            output += f"{website.url}\n"
            for selector in Selector.objects.filter(website_id=website.id):
                output += f"\t{selector.selector_type.name}:{selector.value}\n"
                for item in CollectedData.objects.filter(selector_id=selector.id):
                    parsed_item = item.value.strip().replace('\n', '')
                    output += f"\t\t{parsed_item}\n"
            output += "\n"
        return output

    def export_as_json(self) -> str:
        output = {}
        for website in Website.objects.filter(folder_id=self.folder_id, is_ready=True):
            output[website.url] = {}
            for selector in Selector.objects.filter(website_id=website.id):
                output[website.url][selector.value] = []
                for item in CollectedData.objects.filter(selector_id=selector.id):
                    parsed_item = item.value.strip().replace('\n', '')
                    output[website.url][selector.value].append(parsed_item)
        return json.dumps(output)

    def export_as_xml(self) -> str:
        output = {}
        for website in Website.objects.filter(folder_id=self.folder_id, is_ready=True):
            output[website.url] = {}
            for selector in Selector.objects.filter(website_id=website.id):
                output[website.url][selector.value] = []
                for item in CollectedData.objects.filter(selector_id=selector.id):
                    parsed_item = item.value.strip().replace('\n', '')
                    if json_item := self.__is_json(parsed_item):
                        output[website.url][selector.value].append(json_item)
                    else:
                        output[website.url][selector.value].append(parsed_item)
        xml = dicttoxml(loads(json.dumps(output)))
        return xml

    def export_as_csv(self):
        output = ""
        for website in Website.objects.filter(folder_id=self.folder_id, is_ready=True):
            output += f"{website.url}\n"
            for selector in Selector.objects.filter(website_id=website.id):
                output += f"{selector.selector_type.name.strip()}-{selector.value.strip()}\n"
                for item in CollectedData.objects.filter(selector_id=selector.id):
                    parsed = item.value.replace(",", ".").strip().replace('\n', '')
                    output += f"{parsed},\n"
                output += "\n\n"
        return output

    def __is_json(self, myjson):
        try:
            value = json.loads(myjson)
        except ValueError:
            return False
        return value
