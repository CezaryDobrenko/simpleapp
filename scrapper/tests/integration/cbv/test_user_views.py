from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.user import User
from scrapper.tests.factories import TimezoneFactory, UserFactory


class UserCBVTests(TestCase):
    delete_view = "delete"
    change_password_view = "change_password"
    change_timezone_view = "change_timezone"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_delete_view(self):
        response = self.logged_client.post(
            reverse(self.delete_view, args=(self.user.id,)), follow=True
        )

        assert response.status_code == 200
        assert User.objects.filter(email="email1@test.com").exists() is False

    def test_change_password_view(self):
        old_password = self.user.password
        response = self.logged_client.post(
            reverse(self.change_password_view, args=(self.user.id,)),
            data={
                "old_password": "strong_password",
                "new_password ": "Haslo!1234",
                "new_password_confirm": "Haslo!1234",
                "user_id": self.user.id,
            },
            follow=True,
        )

        self.user.refresh_from_db()
        assert response.status_code == 200
        assert self.user.password != old_password

    def test_change_timezone_view(self):
        new_timezone = TimezoneFactory(name="test", value=5)
        response = self.logged_client.post(
            reverse(self.change_timezone_view, args=(self.user.id,)),
            data={"timezone": new_timezone.id},
            follow=True,
        )

        self.user.refresh_from_db()
        assert response.status_code == 200
        assert self.user.timezone == new_timezone
