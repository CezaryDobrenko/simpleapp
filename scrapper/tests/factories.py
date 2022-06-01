from unittest.mock import MagicMock

import factory
from werkzeug import Request

from scrapper.models.api_key import ApiKey
from scrapper.models.collected_data import CollectedData
from scrapper.models.folder import Folder
from scrapper.models.selector_type import SelectorType
from scrapper.models.selectors import Selector
from scrapper.models.timezone import Timezone
from scrapper.models.user import User
from scrapper.models.website import Website
import time


class RequestFactory:
    def __init__(self, method="GET", headers=None):
        self.request = MagicMock(spec=Request)
        self.request.method = method
        self.request.headers = headers

    def get_request(self):
        return self.request


class TimezoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Timezone

    name = "UTC"
    value = 0


class SelectorTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = SelectorType

    name = "class"
    description = "selektor klasy"


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "Test"
    is_active = True
    email = factory.Sequence(lambda n: f"email{n}@test.com")
    password = factory.PostGenerationMethodCall("set_password", "basepassword")
    timezone = factory.SubFactory(TimezoneFactory)


class FolderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Folder

    name = "folder"
    is_ready = True
    scraping_interval = "MINUTE5"
    last_scraping = None
    user = factory.SubFactory(UserFactory)


class WebsiteFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Website

    url = "https://www.wp.pl/"
    description = "Wirtualna Polska"
    folder = factory.SubFactory(FolderFactory)


class SelectorFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Selector

    value = "test"
    description = "pobiera selektory test"
    website = factory.SubFactory(WebsiteFactory)
    selector_type = factory.SubFactory(SelectorTypeFactory)


class CollectedDataFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CollectedData

    value = "data1"
    selector = factory.SubFactory(SelectorFactory)


class ApiKeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ApiKey

    name = "Klucz API"
    key = "51jdf2i84jsad23912esa"
    is_active = True
    expired_at = "2024-12-26 00:00:00+00"
    user = factory.SubFactory(UserFactory)
