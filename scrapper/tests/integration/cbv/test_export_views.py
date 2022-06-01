from django.test import Client, TestCase
from django.urls import reverse

from scrapper.models.folder import Folder
from scrapper.tests.factories import FolderFactory, UserFactory, WebsiteFactory


class ExportCBVTests(TestCase):
    list_view = "export-list"
    export_json_view = "export-json"
    export_txt_view = "export-txt"
    export_xml_view = "export-xml"
    export_csv_view = "export-csv"

    def setUp(self):
        self.logged_client = Client()
        self.user = UserFactory(email="email1@test.com", password="strong_password")
        self.folder = FolderFactory(user=self.user)
        self.logged_client.login(email="email1@test.com", password="strong_password")

    def test_list_view(self):
        _ = WebsiteFactory(url="www.web_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.web_2.com", folder=self.folder)

        response = self.logged_client.get(reverse(self.list_view))
        expected = list(Folder.objects.all())

        assert response.status_code == 200
        assert list(response.context["object_list"]) == expected

    def test_export_json_view(self):
        _ = WebsiteFactory(url="www.web_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.web_2.com", folder=self.folder)

        response = self.logged_client.get(
            reverse(self.export_json_view, args=(self.folder.id,)), follow=True
        )
        expected = 'attachment; filename="expoted_data.json"'

        assert response.status_code == 200
        assert response["Content-Disposition"] == expected

    def test_export_xml_view(self):
        _ = WebsiteFactory(url="www.web_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.web_2.com", folder=self.folder)

        response = self.logged_client.get(
            reverse(self.export_xml_view, args=(self.folder.id,)), follow=True
        )
        expected = 'attachment; filename="expoted_data.xml"'

        assert response.status_code == 200
        assert response["Content-Disposition"] == expected

    def test_export_txt_view(self):
        _ = WebsiteFactory(url="www.web_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.web_2.com", folder=self.folder)

        response = self.logged_client.get(
            reverse(self.export_txt_view, args=(self.folder.id,)), follow=True
        )
        expected = 'attachment; filename="expoted_data.txt"'

        assert response.status_code == 200
        assert response["Content-Disposition"] == expected

    def test_export_csv_view(self):
        _ = WebsiteFactory(url="www.web_1.com", folder=self.folder)
        _ = WebsiteFactory(url="www.web_2.com", folder=self.folder)

        response = self.logged_client.get(
            reverse(self.export_csv_view, args=(self.folder.id,)), follow=True
        )
        expected = 'attachment; filename="expoted_data.csv"'

        assert response.status_code == 200
        assert response["Content-Disposition"] == expected
