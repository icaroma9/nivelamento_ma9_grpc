from concurrent import futures

import logging

import grpc

from country_pb2_grpc import (
    add_CountryInfoServicer_to_server,
    CountryInfoServicer,
)
from country_pb2 import CountryPagination, Country

import data_utils


class Servicer(CountryInfoServicer):
    def GetPartialCountries(self, request, context):
        results = data_utils.paginate_countries(request.page_number)
        response = CountryPagination(
            countries=results["countries"],
            page_number=results["page_number"],
            last_page=results["last_page"],
        )
        return response

    def SearchCountry(self, request, context):
        country = data_utils.search_country(request.name)
        response = Country(**country)
        return response

    def GetAllCountries(self, request, context):
        for country in data_utils.get_all_countries():
            yield Country(**country)


def serve(block=True):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CountryInfoServicer_to_server(Servicer(), server)
    server.add_insecure_port("[::]:50051")
    server.start()
    if block:
        server.wait_for_termination()
    return server


if __name__ == "__main__":
    logging.basicConfig(level="DEBUG")
    serve()
