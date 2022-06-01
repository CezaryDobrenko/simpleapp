from unittest.mock import ANY

from django.test import TestCase
from graphene.test import Client

from scrapper.graphql import schema
from scrapper.tests.factories import SelectorTypeFactory


class AutocompleteTest(TestCase):
    def setUp(self):
        self.client = Client(schema)

    def test_healthcheck_query(self):
        query = """
            query health_check{
                autocomplete{
                    healthCheck
                }
            }
        """
        expected = {"data": {"autocomplete": {"healthCheck": True}}}

        result = self.client.execute(query)

        assert result == expected

    def test_selectors_type_query(self):
        selector_1 = SelectorTypeFactory(name="id")
        selector_2 = SelectorTypeFactory(name="class")
        selector_3 = SelectorTypeFactory(name="tag")

        query = """
            query selectorTypes{
                autocomplete{
                    selectorTypes{
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
                "autocomplete": {
                    "selectorTypes": {
                        "edges": [
                            {"node": {"name": selector_1.name}},
                            {"node": {"name": selector_2.name}},
                            {"node": {"name": selector_3.name}},
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query)

        assert result == expected

    def test_intervals_query(self):
        query = """
            query Intervals{
                autocomplete{
                    intervals(first: 5){
                        edges{
                            node{
                                intervalValue
                            }
                        }
                    }
                }
            }
        """
        expected = {
            "data": {
                "autocomplete": {
                    "intervals": {
                        "edges": [
                            {"node": {"intervalValue": ANY}},
                            {"node": {"intervalValue": ANY}},
                            {"node": {"intervalValue": ANY}},
                            {"node": {"intervalValue": ANY}},
                            {"node": {"intervalValue": ANY}},
                        ]
                    }
                }
            }
        }

        result = self.client.execute(query)

        assert result == expected
