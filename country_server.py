import logging

logging.getLogger().setLevel('DEBUG')

from concurrent import futures

import grpc

from country_pb2_grpc import add_CountryInfoServicer_to_server, CountryInfoServicer
from country_pb2 import CountryList
import country_data


class Servicer(CountryInfoServicer):
    def GetCountry(self, request, context):
        results = self.paginate_country(request.page_number)
        response = CountryList(
            countries=results['countries'],
            page_number=results['page_number'],
            last_page=results['last_page'],
            )
        return response

    def paginate_country(self, page_number):
        result = {
            "last_page": country_data.last_page,
            "page_number": page_number,
            "countries": [],
        }
        if page_number >= 1:
            result["countries"] = self.get_countries(page_number)
        return result

    def get_countries(self, page_number):
        base = country_data.max_objects * (page_number - 1)
        top = base + country_data.max_objects
        return country_data.df[base:top].to_dict(orient="records")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CountryInfoServicer_to_server(
        Servicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level='DEBUG')
    serve()
