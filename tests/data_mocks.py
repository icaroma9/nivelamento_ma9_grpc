from unittest.mock import Mock

page_mock = {
    "countries": [],
    "page_number": 1,
    "last_page": 1,
}
country_mock = {
    "name": "",
    "code": "",
    "population": 0,
}

data_mock = Mock()
data_mock.paginate_countries = lambda page: page_mock
data_mock.search_country = lambda name: country_mock
data_mock.get_all_countries = lambda: [country_mock]

data_utils = Mock()
data_utils.Data = lambda: data_mock
