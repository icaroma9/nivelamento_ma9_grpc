import unittest
from io import StringIO
import pandas as pd

import data_utils


def load_data_utils():
    csv_string = """
        Name,Code,Population
        Aruba,ABW,54211
        Afghanistan,AFG,8996351
        Angola,AGO,5643182
        Albania,ALB,1608800
        Andorra,AND,13411
        Arab World,ARB,92490932
    """
    data_utils.Data.load_data_info(StringIO(csv_string))


load_data_utils()


class TestLoadData(unittest.TestCase):
    def test_load_data(self):
        data_utils.Data.reset_data_info()
        self.assertTrue(data_utils.Data.df.empty)
        load_data_utils()
        self.assertIsInstance(data_utils.Data.df, pd.DataFrame)
        self.assertIn("name", data_utils.Data.df.columns)
        self.assertIn("code", data_utils.Data.df.columns)
        self.assertIn("population", data_utils.Data.df.columns)


class TestPagination(unittest.TestCase):
    def test_pagination_out_of_bounds(self):
        max_objects = 2
        page_number = -1
        results = data_utils.paginate_countries(page_number, max_objects)
        self.assertFalse(results["countries"])
        self.assertIn("last_page", results)
        self.assertIn("page_number", results)
        self.assertEqual(results["page_number"], page_number)

        max_objects = 200
        page_number = 2
        results = data_utils.paginate_countries(page_number, max_objects)
        self.assertFalse(results["countries"])
        self.assertIn("last_page", results)
        self.assertEqual(results["last_page"], 1)
        self.assertIn("page_number", results)
        self.assertEqual(results["page_number"], page_number)

    def test_pagination_last_page(self):
        max_objects = 2
        results = data_utils.paginate_countries(1, max_objects)
        self.assertEqual(len(results["countries"]), max_objects)
        self.assertGreaterEqual(
            results["last_page"] * max_objects, data_utils.Data.df.shape[0]
        )

    def test_pagination_invalid_page_number(self):
        results = data_utils.paginate_countries(0)
        self.assertFalse(results["countries"])

    def test_pagination_different_results(self):
        country_list_1 = data_utils.paginate_countries(1)["countries"]
        country_list_2 = data_utils.paginate_countries(1)["countries"]
        self.assertEqual(country_list_1, country_list_2)

        country_list_1 = data_utils.paginate_countries(1)["countries"]
        country_list_2 = data_utils.paginate_countries(2)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

        country_list_1 = data_utils.paginate_countries(1)["countries"]
        country_list_2 = data_utils.paginate_countries(3)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

    def test_pagination_base_result_types(self):
        results = data_utils.paginate_countries(1)
        self.assertTrue(results["countries"])
        self.assertIsInstance(results["page_number"], int)
        self.assertIsInstance(results["last_page"], int)
        self.assertIsInstance(results["countries"], list)

    def test_pagination_page_number(self):
        max_objects = 1
        names = []
        for i in range(1, 7):
            result = data_utils.paginate_countries(i, max_objects)
            page_number = result["page_number"]
            self.assertEqual(i, page_number)
            names += [country["name"] for country in result["countries"]]
        self.assertEqual(sorted(names), sorted(list(set(names))))

    def test_pagination_list_result_types(self):
        max_objects = 3
        results = data_utils.paginate_countries(1, max_objects)
        for i in range(0, max_objects):
            country_obj = results["countries"][i]
            self.assertIsInstance(country_obj, dict)
            self.assertIsInstance(country_obj["name"], str)
            self.assertIsInstance(country_obj["code"], str)
            self.assertEqual(len(country_obj["code"]), 3)
            self.assertIsInstance(country_obj["population"], int)


class TestSearch(unittest.TestCase):
    def test_search_success(self):
        result = data_utils.search_country("")
        self.assertIsInstance(result, dict)
        self.assertIn("name", result)
        self.assertIsInstance(result["name"], str)

        self.assertIn("code", result)
        self.assertIsInstance(result["code"], str)

        self.assertIn("population", result)
        try:
            int(result["population"])
        except ValueError:
            self.fail("Population field value can't converted to int")

    def test_search_fail(self):
        result = data_utils.search_country("test")

        self.assertIsInstance(result, dict)
        self.assertFalse(result)


class TestGetAll(unittest.TestCase):
    def test_get_all(self):
        results = data_utils.get_all_countries()
        self.assertIsInstance(results, list)
        self.assertTrue(results)
        self.assertEqual(len(results), data_utils.Data.df.shape[0])
        self.assertEqual(len(results[1]), data_utils.Data.df.shape[1])
