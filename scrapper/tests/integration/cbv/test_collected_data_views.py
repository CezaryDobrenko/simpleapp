from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.collected_data import CollectedData
from scrapper.tests.factories import (
    CollectedDataFactory,
    FolderFactory,
    SelectorFactory,
    UserFactory,
    WebsiteFactory,
)


class CollectedDataCBVTests(TestCase):
    list_view = "collected-data-list"
    delete_view = "collected-data-delete"
    update_view = "collected-data-update"
    clear_view = "collected-data-clear"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.folder = FolderFactory(user=self.user)
        self.website = WebsiteFactory(folder=self.folder)
        self.selector = SelectorFactory(website=self.website)
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = CollectedData(value="data_1", selector=self.selector)
        _ = CollectedData(value="data_2", selector=self.selector)

        response = self.logged_client.get(
            reverse(self.list_view, args=(self.website.id,))
        )
        expected = list(CollectedData.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_delete_view(self):
        collected_data = CollectedDataFactory(value="data_1", selector=self.selector)

        response = self.logged_client.post(
            reverse(self.delete_view, args=(collected_data.id,)), follow=True
        )

        assert response.status_code == 200
        assert CollectedData.objects.filter(value="data_1").exists() is False

    def test_update_view(self):
        collected_data = CollectedDataFactory(value="data_1", selector=self.selector)

        response = self.logged_client.post(
            reverse(self.update_view, args=(collected_data.id,)),
            data={"value": "new_value"},
            follow=True,
        )

        collected_data.refresh_from_db()
        assert response.status_code == 200
        assert collected_data.value == "new_value"

    def test_clear_view(self):
        _ = CollectedData(value="data_1", selector=self.selector)
        _ = CollectedData(value="data_2", selector=self.selector)

        response = self.logged_client.post(
            reverse(self.clear_view, args=(self.selector.id,)),
            follow=True,
        )

        assert response.status_code == 200
        assert CollectedData.objects.count() == 0
