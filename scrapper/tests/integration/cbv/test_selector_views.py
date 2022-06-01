from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.selectors import Selector
from scrapper.tests.factories import (
    FolderFactory,
    SelectorFactory,
    SelectorTypeFactory,
    UserFactory,
    WebsiteFactory,
)


class SelectorCBVTests(TestCase):
    list_view = "selectors-list"
    delete_view = "selectors-delete"
    create_view = "selectors-add"
    update_view = "selectors-update"
    clear_view = "selectors-clear"
    approve_view = "selectors_approve"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.folder = FolderFactory(user=self.user)
        self.website = WebsiteFactory(folder=self.folder)
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = SelectorFactory(value="selector_1", website=self.website)
        _ = SelectorFactory(value="selector_2", website=self.website)

        response = self.logged_client.get(
            reverse(self.list_view, args=(self.website.id,))
        )
        expected = list(Selector.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_delete_view(self):
        selector = SelectorFactory(value="selector_1", website=self.website)

        response = self.logged_client.post(
            reverse(self.delete_view, args=(selector.id,)), follow=True
        )

        assert response.status_code == 200
        assert Selector.objects.filter(value="selector_1").exists() is False

    def test_create_view(self):
        selector_type = SelectorTypeFactory(name="class")
        form_data = {
            "value": "selector_1",
            "description": "opis",
            "selector_type": selector_type.id,
        }

        response = self.logged_client.post(
            reverse(self.create_view, args=(self.website.id,)),
            data=form_data,
            follow=True,
        )

        assert response.status_code == 200
        assert Selector.objects.count() == 1

    def test_update_view(self):
        old_type = SelectorTypeFactory(name="class")
        new_type = SelectorTypeFactory(name="id")
        selector = SelectorFactory(
            value="old_value",
            description="old_desc",
            selector_type=old_type,
            website=self.website,
        )

        response = self.logged_client.post(
            reverse(self.update_view, args=(selector.id,)),
            data={
                "value": "new_value",
                "description": "new_desc",
                "selector_type": new_type.id,
            },
            follow=True,
        )

        selector.refresh_from_db()
        assert response.status_code == 200
        assert selector.value == "new_value"
        assert selector.description == "new_desc"
        assert selector.selector_type == new_type

    def test_clear_view(self):
        _ = SelectorFactory(value="selector_1", website=self.website)
        _ = SelectorFactory(value="selector_2", website=self.website)

        response = self.logged_client.post(
            reverse(self.clear_view, args=(self.website.id,)),
            follow=True,
        )

        assert response.status_code == 200
        assert Selector.objects.count() == 0

    def test_approve_view(self):
        website = WebsiteFactory(
            url="https://www.wp.pl/", is_ready=False, folder=self.folder
        )
        _ = SelectorFactory(value="selector_1", website=website)
        _ = SelectorFactory(value="selector_2", website=website)

        response = self.logged_client.post(
            reverse(self.approve_view, args=(website.id,)),
            follow=True,
        )

        website.refresh_from_db()
        assert response.status_code == 200
        assert website.is_ready is True
