import os

import pandas as pd


class Data:
    df = pd.DataFrame()

    @classmethod
    def reset_data_info(cls):
        cls.df = pd.DataFrame()

    @classmethod
    def load_data_info(cls, file="/data/population_1960.csv"):
        if cls.df.empty:
            if isinstance(file, str):
                dirname = os.path.dirname(__file__)
                dirname = (
                    dirname.replace("\\", "/") if "\\" in dirname else dirname
                )
                file = dirname + file

            cls.df = pd.read_csv(file, sep=",")
            cls.df["Population"] = cls.df["Population"].fillna(0).astype(int)
            cls.df.columns = ["name", "code", "population"]


def search_country(name):
    if Data.df.empty:
        Data.load_data_info()
    result = Data.df[Data.df["name"].str.contains(name, case=False)]
    if result.shape[0] >= 1:
        result = result.iloc[0].to_dict()
    else:
        result = {}
    return result


def paginate_countries(page_number, max_objects=25):
    if Data.df.empty:
        Data.load_data_info()

    last_page = Data.df.shape[0] / max_objects
    last_page = (
        int(last_page) + 1 if isinstance(last_page, float) else last_page
    )

    results = {}
    results["page_number"] = page_number
    results["last_page"] = last_page
    results["countries"] = []
    if page_number >= 1:
        countries = get_all_countries()
        base = max_objects * (page_number - 1)
        top = base + max_objects
        results["countries"] = countries[base:top]
    return results


def get_all_countries():
    if Data.df.empty:
        Data.load_data_info()
    return Data.df.to_dict(orient="records")
