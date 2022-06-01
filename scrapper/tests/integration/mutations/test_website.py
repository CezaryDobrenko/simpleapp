from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import (
    ApiKeyFactory,
    FolderFactory,
    RequestFactory,
    UserFactory,
    WebsiteFactory,
)


class WebsiteTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        folder = FolderFactory(user=user)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.folder = folder
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_authenticated_user_update_website_mutation(self):
        website = WebsiteFactory(
            is_simplified=False,
            is_ready=False,
            description="old_desc",
            folder=self.folder,
        )
        is_ready = "true"
        is_simplified = "true"
        description = "new_desc"

        query = """
            mutation UpdateWebsite{
                updateWebsite(websiteId: "%s", isReady: %s, isSimplified: %s, description: "%s"){
                    website{
                        isSimplified
                        isReady
                        description
                    }
                }
            }
        """ % (
            website.gid,
            is_ready,
            is_simplified,
            description,
        )

        expected = {
            "updateWebsite": {
                "website": {
                    "isSimplified": True,
                    "isReady": True,
                    "description": description,
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_update_other_user_website_mutation(self):
        other_folder = FolderFactory()
        website = WebsiteFactory(folder=other_folder)

        query = """
            mutation UpdateWebsite{
                updateWebsite(websiteId: "%s", isReady: %s, isSimplified: %s, description: "%s"){
                    website{
                        isSimplified
                        isReady
                        description
                    }
                }
            }
        """ % (
            website.gid,
            "true",
            "true",
            "new_desc",
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This website cannot be edited by given api_key"
        )

    def test_authenticated_user_delete_website_mutation(self):
        website = WebsiteFactory(folder=self.folder)
        query = """
            mutation DeleteWebsite{
                deleteWebsite(websiteId: "%s"){
                    isDeleted
                }
            }
        """ % (
            website.gid
        )

        expected = {"deleteWebsite": {"isDeleted": True}}

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_delete_other_user_website_mutation(self):
        other_foler = FolderFactory()
        website = WebsiteFactory(folder=other_foler)
        query = """
            mutation DeleteWebsite{
                deleteWebsite(websiteId: "%s"){
                    isDeleted
                }
            }
        """ % (
            website.gid
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This website cannot be edited by given api_key"
        )
