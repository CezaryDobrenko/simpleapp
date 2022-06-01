from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import (
    ApiKeyFactory,
    FolderFactory,
    RequestFactory,
    UserFactory,
)


class FolderTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_authenticated_user_update_folder_mutation(self):
        folder = FolderFactory(
            name="old_name", is_ready=False, scraping_interval="MINUTE5", user=self.user
        )
        is_ready = "true"
        new_name = "testowy_folder"
        scraping_interval = "HOUR1"
        query = """
            mutation UpdateFolder{
                updateFolder(folderId: "%s", isReady: %s, name: "%s", scrapingInterval: "%s"){
                    folder{
                        name
                        isReady
                        scrapingInterval
                    }
                }
            }
        """ % (
            folder.gid,
            is_ready,
            new_name,
            scraping_interval,
        )

        expected = {
            "updateFolder": {
                "folder": {
                    "name": new_name,
                    "isReady": True,
                    "scrapingInterval": scraping_interval,
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_update_other_user_folder_mutation(self):
        other_user = UserFactory()
        folder = FolderFactory(user=other_user)
        query = """
            mutation UpdateFolder{
                updateFolder(folderId: "%s", isReady: %s, name: "%s", scrapingInterval: "%s"){
                    folder{
                        name
                        isReady
                        scrapingInterval
                    }
                }
            }
        """ % (
            folder.gid,
            "true",
            "new_name",
            "HOUR1",
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This folder cannot be edited by given api_key"
        )

    def test_authenticated_user_delete_folder_mutation(self):
        folder = FolderFactory(user=self.user)
        query = """
            mutation DeleteFolder{
                deleteFolder(folderId: "%s"){
                    isDeleted
                }
            }
        """ % (
            folder.gid
        )

        expected = {"deleteFolder": {"isDeleted": True}}

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_delete_other_user_folder_mutation(self):
        other_user = UserFactory()
        folder = FolderFactory(user=other_user)
        query = """
            mutation DeleteFolder{
                deleteFolder(folderId: "%s"){
                    isDeleted
                }
            }
        """ % (
            folder.gid
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This folder cannot be edited by given api_key"
        )
