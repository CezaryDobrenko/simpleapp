from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.api_key import ApiKey
from scrapper.tests.factories import ApiKeyFactory, UserFactory


class APIKeysCBVTests(TestCase):
    list_view = "api-key-list"
    delete_view = "api-key-delete"
    create_view = "api-key-add"
    update_view = "api-key-update"
    clear_view = "api-key-clear"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = ApiKeyFactory(name="api_key_1", user=self.user)
        _ = ApiKeyFactory(name="api_key_2", user=self.user)

        response = self.logged_client.get(reverse(self.list_view))
        expected = list(ApiKey.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_delete_view(self):
        api_key = ApiKeyFactory(name="api_key_1", user=self.user)

        response = self.logged_client.post(
            reverse(self.delete_view, args=(api_key.id,)), follow=True
        )

        assert response.status_code == 200
        assert ApiKey.objects.filter(name="api_key_1").exists() is False

    def test_clear_view(self):
        _ = ApiKeyFactory(name="api_key_1", user=self.user)
        _ = ApiKeyFactory(name="api_key_2", user=self.user)

        response = self.logged_client.post(reverse(self.clear_view), follow=True)

        assert response.status_code == 200
        assert ApiKey.objects.count() == 0

    def test_create_view(self):
        form_data = {"name": "Nowy klucz", "expired_time": "2022-04-26"}
        response = self.logged_client.post(
            reverse(self.create_view), data=form_data, follow=True
        )

        assert response.status_code == 200
        assert ApiKey.objects.count() == 1

    def test_update_view(self):
        api_key = ApiKeyFactory(
            name="api_key_1", is_active=False, expired_at="2021-03-25", user=self.user
        )

        response = self.logged_client.post(
            reverse(self.update_view, args=(api_key.id,)),
            data={
                "name": "new_api_key_name",
                "is_active": "on",
                "expired_time": "2022-04-26",
            },
            follow=True,
        )

        api_key.refresh_from_db()
        assert response.status_code == 200
        assert api_key.name == "new_api_key_name"
        assert api_key.is_active is True
