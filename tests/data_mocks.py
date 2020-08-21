from unittest.mock import Mock

import data_utils

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

Data_mock = Mock(spec=data_utils.Data)
Data_mock.return_value = Data_mock
Data_mock.paginate_countries.return_value = page_mock
Data_mock.search_country.return_value = country_mock
Data_mock.get_all_countries.return_value = [country_mock]
