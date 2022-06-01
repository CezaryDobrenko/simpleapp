from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import (
    ApiKeyFactory,
    CollectedDataFactory,
    FolderFactory,
    RequestFactory,
    SelectorFactory,
    UserFactory,
    WebsiteFactory,
)


class CollectedDataTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        folder = FolderFactory(name="RetrieveSMS", is_ready=True, user=user)
        website = WebsiteFactory(url="www.scrape.pl", folder=folder)
        selector = SelectorFactory(value="main-text", website=website)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.folder = folder
        self.website = website
        self.selector = selector
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_unauthenticated_user_collected_data_query(self):
        query = """
            query CollectedData{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors(value: "main-text"){
                                                edges{
                                                    node{
                                                        collectedData{
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
                    }
                }
            }
        """

        result = self.client.execute(query)

        assert result["errors"]
        assert result["errors"][0]["message"] == "Invalid request"

    def test_authenticated_user_collected_data_query(self):
        data_1 = CollectedDataFactory(value="data1", selector=self.selector)
        data_2 = CollectedDataFactory(value="data2", selector=self.selector)

        query = """
            query CollectedData{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors(value: "main-text"){
                                                edges{
                                                    node{
                                                        collectedData{
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
                                                                    "collectedData": {
                                                                        "edges": [
                                                                            {
                                                                                "node": {
                                                                                    "value": data_1.value
                                                                                }
                                                                            },
                                                                            {
                                                                                "node": {
                                                                                    "value": data_2.value
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
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected

    def test_authenticated_user_collected_data_filter_query(self):
        other_selector = SelectorFactory()
        _ = CollectedDataFactory(value="main1", selector=self.selector)
        data = CollectedDataFactory(value="test-data", selector=self.selector)
        _ = CollectedDataFactory(value="test-data", selector=other_selector)
        _ = CollectedDataFactory(value="testowa-dana", selector=self.selector)

        query = """
            query CollectedData{
                me{
                    folders(name: "RetrieveSMS"){
                        edges{
                            node{
                                websites(url: "www.scrape.pl"){
                                    edges{
                                        node{
                                            selectors(value: "main-text"){
                                                edges{
                                                    node{
                                                        collectedData(value: "test-"){
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
                                                                    "collectedData": {
                                                                        "edges": [
                                                                            {
                                                                                "node": {
                                                                                    "value": data.value
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
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result == expected
