import unittest

import client
import server

from . import dummies


server.data_utils = dummies.data_utils
page_dummy = dummies.page_dummy
country_dummy = dummies.country_dummy


class TestConnection(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = server.serve(block=False)
        cls.client = client.Client()

    def test_connect_disconnect(self):
        if not self.client.channel:
            self.client.connect()
            self.assertIsNotNone(self.client.channel)
            self.client.disconnect()
            self.assertIsNone(self.client.channel)
        else:
            self.client.disconnect()
            self.assertIsNone(self.client.channel)
            self.client.connect()
            self.assertIsNotNone(self.client.channel)

    def test_get_partial_countries(self):
        page_number = 1
        response = self.client.get_partial_countries(page_number)
        self.assertEqual(list(response.countries), page_dummy["countries"])
        self.assertEqual(response.page_number, page_number)
        self.assertEqual(response.last_page, page_dummy["last_page"])

    def test_search_country(self):
        string = "brazil"
        response = self.client.search_country(string)
        self.assertEqual(response.name, country_dummy["name"])
        self.assertEqual(response.code, country_dummy["code"])
        self.assertEqual(response.population, country_dummy["population"])

    def test_get_all_countries(self):
        for response in self.client.get_all_countries():
            self.assertEqual(response.name, country_dummy["name"])
            self.assertEqual(response.code, country_dummy["code"])
            self.assertEqual(response.population, country_dummy["population"])