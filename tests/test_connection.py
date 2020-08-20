
import unittest

import client
import server

from . import data_mocks


server.data_utils = data_mocks.data_utils
page_mock = data_mocks.page_mock
country_mock = data_mocks.country_mock


class TestConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = server.serve(block=False)

    def test_get_partial_countries(self):
        with client.Connection() as conn:
            page_number = 1
            response = conn.get_partial_countries(page_number)
            self.assertEqual(list(response.countries), page_mock["countries"])
            self.assertEqual(response.page_number, page_number)
            self.assertEqual(response.last_page, page_mock["last_page"])

    def test_search_country(self):
        with client.Connection() as conn:
            string = "brazil"
            response = conn.search_country(string)
            self.assertEqual(response.name, country_mock["name"])
            self.assertEqual(response.code, country_mock["code"])
            self.assertEqual(response.population, country_mock["population"])

    def test_get_all_countries(self):
        with client.Connection() as conn:
            for response in conn.get_all_countries():
                self.assertEqual(response.name, country_mock["name"])
                self.assertEqual(response.code, country_mock["code"])
                self.assertEqual(response.population, country_mock["population"])

    def test_without_connection(self):
        with self.assertRaises(client.ChannelNotCreatedException):
            page_number = 1
            client.Connection().get_partial_countries(page_number)

        with self.assertRaises(client.ChannelNotCreatedException):
            string = "brazil"
            client.Connection().search_country(string)

        with self.assertRaises(client.ChannelNotCreatedException):
            gen = client.Connection().get_all_countries()
            gen.__next__()
