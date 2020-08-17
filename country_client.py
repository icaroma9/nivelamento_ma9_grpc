
import logging

import grpc

import country_pb2
import country_pb2_grpc


def get_country_list(stub):
    page_number = 1
    page_request = country_pb2.PageRequest(page_number=page_number)
    country_list = stub.GetCountry(page_request)
    print(country_list)


def run():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = country_pb2_grpc.CountryInfoStub(channel)
        print("-------------- GetCountry --------------")
        get_country_list(stub)


if __name__ == '__main__':
    logging.basicConfig()
    run()
