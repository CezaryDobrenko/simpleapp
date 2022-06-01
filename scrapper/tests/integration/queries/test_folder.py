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

    def test_unauthenticated_user_folders_query(self):
        query = """
            query Folders{
                me{
                    folders{
                        edges{
                            node{
                                name
                            }
                        }
                    }
                }
            }
        """

        result = self.client.execute(query)

        assert result["errors"]
        assert result["errors"][0]["message"] == "Invalid request"

    def test_authenticated_user_folders_query(self):
        folder_1 = FolderFactory(name="Folder1", user=self.user)
        folder_2 = FolderFactory(name="Folder2", user=self.user)

        query = """
            query Folders{
                me{
                    folders{
                        edges{
                            node{
                                name
                            }
                        }
                    }
                }
            }
        """

        expected = {
            "data": {
                "me": {
                    "folders": {
                        "edges": [
                            {"node": {"name": folder_1.name}},
                            {"node": {"name": folder_2.name}},
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected

    def test_authenticated_user_folders_filter_query(self):
        other_user = UserFactory()
        _ = FolderFactory(name="Pastebin", user=self.user)
        folder = FolderFactory(name="RetrieveSMS", is_ready=True, user=self.user)
        _ = FolderFactory(name="RetrieveOtherUser", is_ready=True, user=other_user)
        _ = FolderFactory(name="RetrievePhone", is_ready=False, user=self.user)

        query = """
            query Folders{
                me{
                    folders(name: "Retrieve", isReady: true){
                        edges{
                            node{
                                name
                            }
                        }
                    }
                }
            }
        """

        expected = {
            "data": {"me": {"folders": {"edges": [{"node": {"name": folder.name}}]}}}
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected
