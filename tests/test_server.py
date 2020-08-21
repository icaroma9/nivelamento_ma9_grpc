import unittest
from unittest.mock import Mock, patch

import country_pb2
import server
from . import data_mocks


@patch("server.data_utils.Data", data_mocks.Data_mock)
class TestCountryPagination(unittest.TestCase):
    def test_partial_countries(self):
        servicer = server.Servicer()
        request = Mock()
        request.page_number = 1

        response = servicer.GetPartialCountries(request, {})
        self.assertIsInstance(response, country_pb2.CountryPagination)

        try:
            getattr(response, "countries")
        except AttributeError:
            self.fail("Response has no countries attribute")

        self.assertEqual(
            list(response.countries), data_mocks.page_mock["countries"]
        )

        try:
            getattr(response, "page_number")
        except AttributeError:
            self.fail("Response has no page_number attribute")
        self.assertEqual(response.page_number, request.page_number)

        try:
            getattr(response, "last_page")
        except AttributeError:
            self.fail("Response has no last_page attribute")
        self.assertEqual(response.last_page, data_mocks.page_mock["last_page"])

    def test_search_country(self):
        servicer = server.Servicer()
        request = Mock()
        request.name = "test"
        response = servicer.SearchCountry(request, {})
        self.assertIsInstance(response, country_pb2.Country)

        try:
            getattr(response, "name")
        except AttributeError:
            self.fail("Response has no name attribute")
        self.assertEqual(response.name, data_mocks.country_mock["name"])

        try:
            getattr(response, "code")
        except AttributeError:
            self.fail("Response has no code attribute")
        self.assertEqual(response.code, data_mocks.country_mock["code"])

        try:
            getattr(response, "population")
        except AttributeError:
            self.fail("Response has no population attribute")
        self.assertEqual(
            response.population, data_mocks.country_mock["population"]
        )

    def test_get_all_countries(self):
        servicer = server.Servicer()
        for response in servicer.GetAllCountries({}, {}):
            self.assertIsInstance(response, country_pb2.Country)

            try:
                getattr(response, "name")
            except AttributeError:
                self.fail("Response has no name attribute")
            self.assertEqual(response.name, data_mocks.country_mock["name"])

            try:
                getattr(response, "code")
            except AttributeError:
                self.fail("Response has no code attribute")
            self.assertEqual(response.code, data_mocks.country_mock["code"])

            try:
                getattr(response, "population")
            except AttributeError:
                self.fail("Response has no population attribute")
            self.assertEqual(
                response.population, data_mocks.country_mock["population"]
            )


@patch("server.data_utils.Data", data_mocks.Data_mock)
class TestServe(unittest.TestCase):
    def test_serve(self):
        servicer = server.serve(block=False)
        with self.assertRaises(ValueError):
            servicer.start()
