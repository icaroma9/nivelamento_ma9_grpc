import grpc

import country_pb2
import country_pb2_grpc


class Client:
    def __init__(self):
        self.channel = None
        self.stub = None

    def connect(self):
        if not self.channel:
            self.channel = grpc.insecure_channel("localhost:50051")
            self.stub = country_pb2_grpc.CountryInfoStub(self.channel)

    def disconnect(self):
        if self.channel:
            self.channel.close()
            self.channel = None
            self.stub = None

    def get_partial_countries(self, page_number):
        self.connect()
        page = country_pb2.Page(page_number=page_number)
        response = self.stub.GetPartialCountries(page)
        self.disconnect()

        return response

    def search_country(self, name):
        self.connect()
        country_name = country_pb2.CountryName(name=name)
        response = self.stub.SearchCountry(country_name)
        self.disconnect()

        return response

    def get_all_countries(self):
        self.connect()
        empty = country_pb2.Empty()
        for response in self.stub.GetAllCountries(empty):
            yield response
        self.disconnect()
