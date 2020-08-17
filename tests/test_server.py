import unittest
from unittest.mock import Mock

import country_pb2
import server
from . import dummies

server.data_utils = dummies.data_utils
page_dummy = dummies.page_dummy
country_dummy = dummies.country_dummy


class TestCountryPagination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = server.Servicer()

    def test_partial_countries(self):
        request = Mock()
        request.page_number = 1

        response = self.server.GetPartialCountries(request, {})
        self.assertIsInstance(response, country_pb2.CountryPagination)

        try:
            getattr(response, "countries")
        except AttributeError:
            self.fail("Response has no countries attribute")

        self.assertEqual(list(response.countries), page_dummy["countries"])

        try:
            getattr(response, "page_number")
        except AttributeError:
            self.fail("Response has no page_number attribute")
        self.assertEqual(response.page_number, request.page_number)

        try:
            getattr(response, "last_page")
        except AttributeError:
            self.fail("Response has no last_page attribute")
        self.assertEqual(response.last_page, page_dummy["last_page"])

    def test_search_country(self):
        request = Mock()
        request.name = "test"

        response = self.server.SearchCountry(request, {})
        self.assertIsInstance(response, country_pb2.Country)

        try:
            getattr(response, "name")
        except AttributeError:
            self.fail("Response has no name attribute")
        self.assertEqual(response.name, country_dummy["name"])

        try:
            getattr(response, "code")
        except AttributeError:
            self.fail("Response has no code attribute")
        self.assertEqual(response.code, country_dummy["code"])

        try:
            getattr(response, "population")
        except AttributeError:
            self.fail("Response has no population attribute")
        self.assertEqual(response.population, country_dummy["population"])

    def test_get_all_countries(self):
        for response in self.server.GetAllCountries({}, {}):
            self.assertIsInstance(response, country_pb2.Country)

            try:
                getattr(response, "name")
            except AttributeError:
                self.fail("Response has no name attribute")
            self.assertEqual(response.name, country_dummy["name"])

            try:
                getattr(response, "code")
            except AttributeError:
                self.fail("Response has no code attribute")
            self.assertEqual(response.code, country_dummy["code"])

            try:
                getattr(response, "population")
            except AttributeError:
                self.fail("Response has no population attribute")
            self.assertEqual(response.population, country_dummy["population"])


class TestServe(unittest.TestCase):
    def test_serve(self):
        self.server = server.serve(block=False)
        with self.assertRaises(ValueError):
            self.server.start()
