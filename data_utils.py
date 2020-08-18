import os

from io import StringIO

import pandas as pd


class Data:
    def __init__(
        self, rel_file_path="/data/population_1960.csv", buffer_string=None
    ):
        self.df = pd.DataFrame()
        self.buffer_string = buffer_string
        dirname = os.path.dirname(__file__)
        dirname = dirname.replace("\\", "/") if "\\" in dirname else dirname
        self.file = dirname + rel_file_path

        self.load_data_info()

    def reset_data_info(self):
        self.df = pd.DataFrame()

    def load_data_info(self):
        if self.df.empty:
            data = self.file
            if self.buffer_string:
                data = StringIO(self.buffer_string)
            self.df = pd.read_csv(data, sep=",")
            self.df["Population"] = self.df["Population"].fillna(0).astype(int)
            self.df.columns = ["name", "code", "population"]

    def search_country(self, name):
        if self.df.empty:
            self.load_data_info()
        result = self.df[self.df["name"].str.contains(name, case=False)]
        if result.shape[0] >= 1:
            result = result.iloc[0].to_dict()
        else:
            result = {}
        return result

    def paginate_countries(self, page_number, max_objects=25):
        if self.df.empty:
            self.load_data_info()

        last_page = self.df.shape[0] / max_objects
        last_page = (
            int(last_page) + 1 if isinstance(last_page, float) else last_page
        )

        results = {}
        results["page_number"] = page_number
        results["last_page"] = last_page
        results["countries"] = []
        if page_number >= 1:
            countries = self.get_all_countries()
            base = max_objects * (page_number - 1)
            top = base + max_objects
            results["countries"] = countries[base:top]
        return results

    def get_all_countries(self):
        if self.df.empty:
            self.load_data_info()
        return self.df.to_dict(orient="records")
