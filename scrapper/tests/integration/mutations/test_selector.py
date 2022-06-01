from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import (
    ApiKeyFactory,
    CollectedDataFactory,
    FolderFactory,
    RequestFactory,
    SelectorFactory,
    SelectorTypeFactory,
    UserFactory,
    WebsiteFactory,
)


class SelectorTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        folder = FolderFactory(user=user)
        website = WebsiteFactory(folder=folder)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.folder = folder
        self.website = website
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_authenticated_user_update_selector_mutation(self):
        selector = SelectorFactory(
            value="old_value", description="old_desc", website=self.website
        )
        value = "new_value"
        description = "new_desc"
        type = SelectorTypeFactory(name="new_type")

        query = """
            mutation UpdateSelector{
                updateSelector(selectorId: "%s", value: "%s", description: "%s", selectorType: "%s"){
                    selector{
                        value
                        description
                        selectorType{
                            name
                        }
                    }
                }
            }
        """ % (
            selector.gid,
            value,
            description,
            type.gid,
        )

        expected = {
            "updateSelector": {
                "selector": {
                    "value": value,
                    "description": description,
                    "selectorType": {"name": type.name},
                }
            }
        }

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_update_other_user_selector_mutation(self):
        other_website = WebsiteFactory()
        selector = SelectorFactory(website=other_website)

        query = """
            mutation UpdateSelector{
                updateSelector(selectorId: "%s", value: "%s", description: "%s"){
                    selector{
                        value
                        description
                    }
                }
            }
        """ % (
            selector.gid,
            "new_value",
            "new_desc",
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This selector cannot be edited by given api_key"
        )

    def test_authenticated_user_delete_selector_mutation(self):
        selector = SelectorFactory(website=self.website)

        query = """
            mutation DeleteSelector{
                deleteSelector(selectorId: "%s"){
                    isDeleted
                }
            }
        """ % (
            selector.gid
        )

        expected = {"deleteSelector": {"isDeleted": True}}

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_delete_other_user_selector_mutation(self):
        other_website = WebsiteFactory()
        selector = SelectorFactory(website=other_website)

        query = """
            mutation DeleteSelector{
                deleteSelector(selectorId: "%s"){
                    isDeleted
                }
            }
        """ % (
            selector.gid
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This selector cannot be edited by given api_key"
        )

    def test_authenticated_user_clear_selector_data_mutation(self):
        selector = SelectorFactory(website=self.website)
        _ = CollectedDataFactory(value="data1", selector=selector)
        _ = CollectedDataFactory(value="data2", selector=selector)

        query = """
            mutation ClearSelectorData{
                clearSelectorData(selectorId: "%s"){
                    selector{
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
        """ % (
            selector.gid
        )
        expected = {"clearSelectorData": {"selector": {"collectedData": {"edges": []}}}}

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_authenticated_user_clear_other_user_selector_data_mutation(self):
        other_website = WebsiteFactory()
        selector = SelectorFactory(website=other_website)

        query = """
            mutation ClearSelectorData{
                clearSelectorData(selectorId: "%s"){
                    selector{
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
        """ % (
            selector.gid
        )

        result = self.client.execute(query, context_value={"request": self.request})

        assert result.get("errors")
        assert (
            result["errors"][0]["message"]
            == "This selector cannot be edited by given api_key"
        )
