from django.test import Client, TestCase
from django.urls import reverse

from scrapper.tests.factories import FolderFactory, UserFactory, WebsiteFactory


class InfoPageCBVTests(TestCase):
    dashboard_view = "dashboard"
    private_dashboard_view = "private_dashboard"
    mission_view = "mission"
    announcement_view = "announcements"
    process_view = "process"
    news_view = "news"
    news_clear_view = "news-clear"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.folder = FolderFactory(user=self.user)
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_dashboard_view(self):
        response = self.logged_client.get(reverse(self.dashboard_view))

        assert response.status_code == 200

    def test_private_dashboard_view(self):
        response = self.logged_client.get(reverse(self.private_dashboard_view))

        assert response.status_code == 200

    def test_mission_view(self):
        response = self.logged_client.get(reverse(self.mission_view))

        assert response.status_code == 200

    def test_announcement_view(self):
        response = self.logged_client.get(reverse(self.announcement_view))

        assert response.status_code == 200

    def test_process_view(self):
        response = self.logged_client.get(reverse(self.process_view))

        assert response.status_code == 200

    def test_news_view(self):
        _ = WebsiteFactory(
            url="www.test.com",
            is_new_data_collected=True,
            is_valid_with_robots=False,
            folder=self.folder,
        )
        _ = WebsiteFactory(
            url="www.test2.com",
            is_new_data_collected=True,
            is_valid_with_robots=True,
            folder=self.folder,
        )

        response = self.logged_client.get(reverse(self.news_view))

        assert response.status_code == 200
        assert len(response.context["object_list"]) == 2
        assert len(response.context["warnings"]) == 1

    def test_news_clear_view(self):
        web1 = WebsiteFactory(
            url="www.test.com",
            is_new_data_collected=True,
            is_valid_with_robots=False,
            folder=self.folder,
        )
        web2 = WebsiteFactory(
            url="www.test2.com",
            is_new_data_collected=True,
            is_valid_with_robots=True,
            folder=self.folder,
        )

        response = self.logged_client.post(
            reverse(self.news_clear_view, args=(self.user.id,)), follow=True
        )

        web1.refresh_from_db()
        web2.refresh_from_db()
        assert response.status_code == 200
        assert web1.is_new_data_collected is False
        assert web2.is_new_data_collected is False
        assert web1.is_valid_with_robots is False
        assert web2.is_valid_with_robots is True
