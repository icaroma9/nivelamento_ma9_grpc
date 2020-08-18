import unittest

import pandas as pd

import data_utils

test_file = "/tests/test.csv"


class DataTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        string = """
            Name,Code,Population
            Aruba,ABW,54211
            Afghanistan,AFG,8996351
            Angola,AGO,5643182
            Albania,ALB,1608800
            Andorra,AND,13411
            Arab World,ARB,92490932
        """
        cls.data = data_utils.Data(buffer_string=string)


class TestDataInit(DataTestCase):
    def test_load_data_buffer(self):
        self.data.reset_data_info()
        self.assertTrue(self.data.df.empty)
        self.data.load_data_info()
        self.assertIsInstance(self.data.df, pd.DataFrame)
        self.assertIn("name", self.data.df.columns)
        self.assertIn("code", self.data.df.columns)
        self.assertIn("population", self.data.df.columns)

    def test_load_data_csv(self):
        data = data_utils.Data(rel_file_path=test_file)
        self.assertFalse(data.df.empty)

        data.reset_data_info()
        self.assertTrue(data.df.empty)
        data.load_data_info()
        self.assertIsInstance(data.df, pd.DataFrame)
        self.assertIn("name", data.df.columns)
        self.assertIn("code", data.df.columns)
        self.assertIn("population", data.df.columns)


class TestPagination(DataTestCase):
    def test_pagination_out_of_bounds(self):
        max_objects = 2
        page_number = -1
        results = self.data.paginate_countries(page_number, max_objects)
        self.assertFalse(results["countries"])
        self.assertIn("last_page", results)
        self.assertIn("page_number", results)
        self.assertEqual(results["page_number"], page_number)

        max_objects = 200
        page_number = 2
        results = self.data.paginate_countries(page_number, max_objects)
        self.assertFalse(results["countries"])
        self.assertIn("last_page", results)
        self.assertEqual(results["last_page"], 1)
        self.assertIn("page_number", results)
        self.assertEqual(results["page_number"], page_number)

    def test_pagination_last_page(self):
        max_objects = 2
        results = self.data.paginate_countries(1, max_objects)
        self.assertEqual(len(results["countries"]), max_objects)
        self.assertGreaterEqual(
            results["last_page"] * max_objects, self.data.df.shape[0]
        )

    def test_pagination_invalid_page_number(self):
        results = self.data.paginate_countries(0)
        self.assertFalse(results["countries"])

    def test_pagination_different_results(self):
        country_list_1 = self.data.paginate_countries(1)["countries"]
        country_list_2 = self.data.paginate_countries(1)["countries"]
        self.assertEqual(country_list_1, country_list_2)

        country_list_1 = self.data.paginate_countries(1)["countries"]
        country_list_2 = self.data.paginate_countries(2)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

        country_list_1 = self.data.paginate_countries(1)["countries"]
        country_list_2 = self.data.paginate_countries(3)["countries"]
        self.assertNotEqual(country_list_1, country_list_2)

    def test_pagination_base_result_types(self):
        results = self.data.paginate_countries(1)
        self.assertTrue(results["countries"])
        self.assertIsInstance(results["page_number"], int)
        self.assertIsInstance(results["last_page"], int)
        self.assertIsInstance(results["countries"], list)

    def test_pagination_page_number(self):
        max_objects = 1
        names = []
        for i in range(1, 7):
            result = self.data.paginate_countries(i, max_objects)
            page_number = result["page_number"]
            self.assertEqual(i, page_number)
            names += [country["name"] for country in result["countries"]]
        self.assertEqual(sorted(names), sorted(list(set(names))))

    def test_pagination_list_result_types(self):
        max_objects = 3
        results = self.data.paginate_countries(1, max_objects)
        for i in range(0, max_objects):
            country_obj = results["countries"][i]
            self.assertIsInstance(country_obj, dict)
            self.assertIsInstance(country_obj["name"], str)
            self.assertIsInstance(country_obj["code"], str)
            self.assertEqual(len(country_obj["code"]), 3)
            self.assertIsInstance(country_obj["population"], int)


class TestSearch(DataTestCase):
    def test_search_success(self):
        result = self.data.search_country("")
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
        result = self.data.search_country("test")

        self.assertIsInstance(result, dict)
        self.assertFalse(result)


class TestGetAll(DataTestCase):
    def test_get_all(self):
        results = self.data.get_all_countries()
        self.assertIsInstance(results, list)
        self.assertTrue(results)
        self.assertEqual(len(results), self.data.df.shape[0])
        self.assertEqual(len(results[1]), self.data.df.shape[1])
