import grpc

import country_pb2
import country_pb2_grpc


class ChannelNotCreatedException(Exception):
    pass


class Connection:
    def __init__(self):
        self.channel = None
        self.stub = None

    def __enter__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = country_pb2_grpc.CountryInfoStub(self.channel)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.channel.close()

    def get_partial_countries(self, page_number):
        if not self.channel:
            raise ChannelNotCreatedException("Channel isn't created")
        page = country_pb2.Page(page_number=page_number)
        response = self.stub.GetPartialCountries(page)
        return response

    def search_country(self, name):
        if not self.channel:
            raise ChannelNotCreatedException("Channel isn't created")
        country_name = country_pb2.CountryName(name=name)
        response = self.stub.SearchCountry(country_name)
        return response

    def get_all_countries(self):
        if not self.channel:
            raise ChannelNotCreatedException("Channel isn't created")
        empty = country_pb2.Empty()
        for response in self.stub.GetAllCountries(empty):
            yield response
