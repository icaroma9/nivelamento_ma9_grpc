from unittest.mock import Mock

page_dummy = {
    "countries": [],
    "page_number": 1,
    "last_page": 1,
}
country_dummy = {
    "name": "",
    "code": "",
    "population": 0,
}

data_dummy = Mock()
data_dummy.paginate_countries = lambda page: page_dummy
data_dummy.search_country = lambda name: country_dummy
data_dummy.get_all_countries = lambda: [country_dummy]

data_utils = Mock()
data_utils.Data = lambda: data_dummy
