import unittest
from unittest.mock import patch

import client
import server

from . import data_mocks


@patch("server.data_utils.Data", data_mocks.Data_mock)
class TestConnection(unittest.TestCase):
    def test_get_partial_countries(self):
        server.serve(block=False)

        with client.Connection() as conn:
            page_number = 1
            response = conn.get_partial_countries(page_number)
            self.assertEqual(
                list(response.countries), data_mocks.page_mock["countries"]
            )
            self.assertEqual(response.page_number, page_number)
            self.assertEqual(
                response.last_page, data_mocks.page_mock["last_page"]
            )

    def test_search_country(self):
        server.serve(block=False)

        with client.Connection() as conn:
            string = "brazil"
            response = conn.search_country(string)
            self.assertEqual(response.name, data_mocks.country_mock["name"])
            self.assertEqual(response.code, data_mocks.country_mock["code"])
            self.assertEqual(
                response.population, data_mocks.country_mock["population"]
            )

    def test_get_all_countries(self):
        server.serve(block=False)

        with client.Connection() as conn:
            for response in conn.get_all_countries():
                self.assertEqual(response.name, data_mocks.country_mock["name"])
                self.assertEqual(response.code, data_mocks.country_mock["code"])
                self.assertEqual(
                    response.population, data_mocks.country_mock["population"]
                )

    def test_without_connection(self):
        server.serve(block=False)

        with self.assertRaises(client.ChannelNotCreatedException):
            page_number = 1
            client.Connection().get_partial_countries(page_number)

        with self.assertRaises(client.ChannelNotCreatedException):
            string = "brazil"
            client.Connection().search_country(string)

        with self.assertRaises(client.ChannelNotCreatedException):
            gen = client.Connection().get_all_countries()
            gen.__next__()
