from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.folder import Folder
from scrapper.tests.factories import FolderFactory, UserFactory


class FolderCBVTests(TestCase):
    list_view = "folders"
    delete_view = "folders-delete"
    create_view = "folders-add"
    update_view = "folders-update"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = FolderFactory(name="folder_1", user=self.user)
        _ = FolderFactory(name="folder_2", user=self.user)

        response = self.logged_client.get(reverse(self.list_view))
        expected = list(Folder.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_delete_view(self):
        folder = FolderFactory(name="folder_1", user=self.user)

        response = self.logged_client.post(
            reverse(self.delete_view, args=(folder.id,)), follow=True
        )

        assert response.status_code == 200
        assert Folder.objects.filter(name="folder_1").exists() is False

    def test_create_view(self):
        form_data = {
            "name": "Nowy folder",
            "is_ready": "on",
            "scraping_interval": "HOUR1",
        }

        response = self.logged_client.post(
            reverse(self.create_view), data=form_data, follow=True
        )

        assert response.status_code == 200
        assert Folder.objects.count() == 1

    def test_update_view(self):
        folder = FolderFactory(name="folder_1", user=self.user)

        response = self.logged_client.post(
            reverse(self.update_view, args=(folder.id,)),
            data={
                "name": "Nowa nazwa",
                "is_ready": "False",
                "scraping_interval": "HOUR1",
            },
            follow=True,
        )

        folder.refresh_from_db()
        assert response.status_code == 200
        assert folder.name == "Nowa nazwa"
        assert folder.is_ready is False
