from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.website import Website
from scrapper.tests.factories import FolderFactory, UserFactory, WebsiteFactory


class WebsiteCBVTests(TestCase):
    list_view = "websites"
    creator_list_view = "websites-settings"
    delete_view = "websites-delete"
    create_view = "websites-add"
    update_view = "websites-update"
    clear_view = "websites-clear"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.folder = FolderFactory(user=self.user)
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = WebsiteFactory(url="www.website_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.website_2.com", folder=self.folder)

        response = self.logged_client.get(reverse(self.list_view))
        expected = list(Website.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_creator_list_view(self):
        _ = WebsiteFactory(url="www.website_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.website_2.com", folder=self.folder)

        response = self.logged_client.get(
            reverse(self.creator_list_view, args=(self.folder.id,))
        )
        expected = list(Website.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_delete_view(self):
        website = WebsiteFactory(url="www.website_1.com", folder=self.folder)

        response = self.logged_client.post(
            reverse(self.delete_view, args=(website.id,)), follow=True
        )

        assert response.status_code == 200
        assert Website.objects.filter(url="www.website_1.com").exists() is False

    def test_create_view(self):
        form_data = {
            "url": "https://www.wp.pl/",
            "description": "opis",
            "is_ready": "on",
            "is_simplified": "on",
        }

        response = self.logged_client.post(
            reverse(self.create_view, args=(self.folder.id,)),
            data=form_data,
            follow=True,
        )

        assert response.status_code == 200
        assert Website.objects.count() == 1

    def test_update_view(self):
        website = WebsiteFactory(
            url="www.website_1.com",
            description="old_desc",
            is_ready=False,
            is_simplified=False,
            folder=self.folder,
        )

        response = self.logged_client.post(
            reverse(self.update_view, args=(website.id,)),
            data={
                "url": "https://www.wp.pl/",
                "description": "opis",
                "is_ready": "on",
                "is_simplified": "on",
            },
            follow=True,
        )

        website.refresh_from_db()
        assert response.status_code == 200
        assert website.url == "https://www.wp.pl/"
        assert website.description == "opis"
        assert website.is_ready is True
        assert website.is_simplified is True

    def test_clear_view(self):
        _ = WebsiteFactory(url="www.website_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.website_2.com", folder=self.folder)

        response = self.logged_client.post(
            reverse(self.clear_view, args=(self.folder.id,)),
            follow=True,
        )

        assert response.status_code == 200
        assert Website.objects.count() == 0
