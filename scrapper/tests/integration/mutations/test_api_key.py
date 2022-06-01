from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import ApiKeyFactory, RequestFactory, UserFactory


class ApiKeyTest(TestCase):
    def setUp(self):
        user = UserFactory()
        api_key = ApiKeyFactory(key="51jdf2i84jsad23912esa", user=user)
        request_factory = RequestFactory(
            method="GET", headers={"Authorization": f"Bearer {api_key.key}"}
        )
        self.user = user
        self.api_key = api_key
        self.client = Client(schema)
        self.request = request_factory.get_request()

    def test_authenticated_user_deactivate_api_key_mutation(self):
        query = """
            mutation DeactivateApiKey{
                deactivateApiKey{
                    isDeactivated
                }
            }
        """

        expected = {"deactivateApiKey": {"isDeactivated": True}}

        result = self.client.execute(query, context_value={"request": self.request})

        assert not result.get("errors")
        assert result["data"] == expected

    def test_unauthenticated_user_deactivate_api_key_mutation(self):
        query = """
            mutation DeactivateApiKey{
                deactivateApiKey{
                    isDeactivated
                }
            }
        """

        result = self.client.execute(query)

        assert result.get("errors")
        assert result["errors"][0]["message"] == "Invalid request"
