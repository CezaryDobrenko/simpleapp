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
        folder = FolderFactory(name="RetrieveSMS", is_ready=True, user=user)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.folder = folder
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_unauthenticated_user_websites_query(self):
        query = """
            query Websites{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites{
                                    edges{
                                        node{
                                            url
                                        }
                                    }
                                }
                            }
                        }
                    }
                }
            }
        """

        result = self.client.execute(query)

        assert result["errors"]
        assert result["errors"][0]["message"] == "Invalid request"

    def test_authenticated_user_websites_query(self):
        web_1 = WebsiteFactory(url="www.test1.com", folder=self.folder)
        web_2 = WebsiteFactory(url="www.test2.com", folder=self.folder)

        query = """
            query Websites{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites{
                                    edges{
                                        node{
                                            url
                                        }
                                    }
                                }
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
                            {
                                "node": {
                                    "websites": {
                                        "edges": [
                                            {"node": {"url": web_1.url}},
                                            {"node": {"url": web_2.url}},
                                        ]
                                    }
                                }
                            }
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected

    def test_authenticated_user_websites_filter_query(self):
        other_folder = FolderFactory()
        _ = WebsiteFactory(url="www.wp.pl", is_ready=True, folder=self.folder)
        web = WebsiteFactory(url="www.scrap.com", is_ready=True, folder=self.folder)
        _ = WebsiteFactory(url="www.test-scrap.com", is_ready=True, folder=other_folder)
        _ = WebsiteFactory(url="www.pastebin.com", is_ready=False, folder=self.folder)

        query = """
            query Websites{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "scrap", isReady: true){
                                    edges{
                                        node{
                                            url
                                        }
                                    }
                                }
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
                            {
                                "node": {
                                    "websites": {"edges": [{"node": {"url": web.url}}]}
                                }
                            }
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected
