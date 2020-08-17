import unittest

import country_server
import country_data


class TestCountryPagination(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.server = country_server.Servicer()

    def test_pagination_number(self):
        results = self.server.paginate_country(1)
        self.assertEqual(len(results["countries"]), country_data.max_objects)
        self.assertGreaterEqual(
            results["last_page"] * country_data.max_objects, country_data.df.shape[0]
        )

    def test_pagination_invalid_page_number(self):
        results = self.server.paginate_country(0)
        self.assertFalse(results["countries"])

    def test_pagination_different_results(self):
        country_list_1 = self.server.paginate_country(1)["countries"]
        country_list_2 = self.server.paginate_country(1)["countries"]
        self.assertEqual(country_list_1, country_list_2)

        country_list_1 = self.server.paginate_country(1)["countries"]
        country_list_2 = self.server.paginate_country(2)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

        country_list_1 = self.server.paginate_country(1)["countries"]
        country_list_2 = self.server.paginate_country(3)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

    def test_pagination_base_result_types(self):
        results = self.server.paginate_country(1)
        self.assertTrue(results["countries"])
        self.assertIsInstance(results["page_number"], int)
        self.assertIsInstance(results["last_page"], int)
        self.assertIsInstance(results["countries"], list)

    def test_pagination_page_number(self):
        for i in range(0, country_data.max_objects):
            page_number = self.server.paginate_country(i)["page_number"]
            self.assertEqual(i, page_number)

    def test_pagination_list_result_types(self):
        results = self.server.paginate_country(1)
        for i in range(0, country_data.max_objects):
            country_obj = results["countries"][i]
            self.assertIsInstance(country_obj, dict)
            self.assertIsInstance(country_obj["name"], str)
            self.assertIsInstance(country_obj["code"], str)
            self.assertEqual(len(country_obj["code"]), 3)
            self.assertIsInstance(country_obj["population"], int)
