from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import (
    ApiKeyFactory,
    FolderFactory,
    RequestFactory,
    SelectorFactory,
    UserFactory,
    WebsiteFactory,
)


class SelectorTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        folder = FolderFactory(name="RetrieveSMS", is_ready=True, user=user)
        website = WebsiteFactory(url="www.scrape.pl", folder=folder)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.folder = folder
        self.website = website
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_unauthenticated_user_selectors_query(self):
        query = """
            query Selectors{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors{
                                                edges{
                                                    node{
                                                        value
                                                    }
                                                }
                                            }
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

    def test_authenticated_user_selectors_query(self):
        selector_1 = SelectorFactory(value="header-main", website=self.website)
        selector_2 = SelectorFactory(value="sub-nav", website=self.website)

        query = """
            query Selectors{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors{
                                                edges{
                                                    node{
                                                        value
                                                    }
                                                }
                                            }
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
                                            {
                                                "node": {
                                                    "selectors": {
                                                        "edges": [
                                                            {
                                                                "node": {
                                                                    "value": selector_1.value
                                                                }
                                                            },
                                                            {
                                                                "node": {
                                                                    "value": selector_2.value
                                                                }
                                                            },
                                                        ]
                                                    }
                                                }
                                            }
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

    def test_authenticated_user_selectors_filter_query(self):
        other_website = WebsiteFactory()
        _ = SelectorFactory(value="nav", website=self.website)
        selector = SelectorFactory(value="pager", website=self.website)
        _ = SelectorFactory(value="title-text", website=other_website)
        _ = SelectorFactory(value="testamonials", website=self.website)

        query = """
            query Selectors{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors(value: "pager"){
                                                edges{
                                                    node{
                                                        value
                                                    }
                                                }
                                            }
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
                                            {
                                                "node": {
                                                    "selectors": {
                                                        "edges": [
                                                            {
                                                                "node": {
                                                                    "value": selector.value
                                                                }
                                                            }
                                                        ]
                                                    }
                                                }
                                            }
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
