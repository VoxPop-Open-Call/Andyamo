import sys 
import timeit

from concurrent import futures
import logging
import math
import time
import json

import grpc
import route_service_pb2
import route_service_pb2_grpc

from andyamo import types

import c_foot
import c_manual_wheelchair
import c_electric_wheelchair

import access



class RouteServiceServicer(route_service_pb2_grpc.RouteService):
    """Provides methods that implement functionality of routing server."""

    def __init__(self):
        pass

    def ShortestPath(self, request, context):

        _profile = request.profile.profile
        profile_as_str = route_service_pb2._PROFILE_PROFILE.values_by_number[_profile].name
        profile = types.Profile[profile_as_str]

        if profile == types.Profile.FOOT:
            res = c_foot.get_route(request.start, request.end)
            
        elif profile == types.Profile.MANUAL_WHEELCHAIR:
            res = c_manual_wheelchair.get_route(request.start, request.end)

        elif profile == types.Profile.ELECTRIC_WHEELCHAIR:
            res = c_electric_wheelchair.get_route(request.start, request.end)

        else:
            raise NotImplementedError

        route_str, distance_str = res.split(":")
        
        route = route_str.strip().split(" ")
        distance = int(distance_str.strip())
        return route_service_pb2.RouteResponse(route=route, distance=distance)

    def ListNodes(self, request, context):
        _profile = request.profile
        profile_as_str = route_service_pb2._PROFILE_PROFILE.values_by_number[_profile].name
        print(profile_as_str)

        profile = types.Profile[profile_as_str]

        with open("data.json", "r") as f:
            for line in f.readlines():
                feature = json.loads(line.strip())
                if access.is_accessible(feature, profile):
                    coords = feature["feature"]["geometry"]["coordinates"]
                    indexes = feature["feature"]["properties"]["nodes"]
                    for coord, index  in zip(coords, indexes):
                        yield route_service_pb2.Node(index=f"id_{index}", latitude=coord[1], longitude=coord[0])
                
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    route_service_pb2_grpc.add_RouteServiceServicer_to_server(
        RouteServiceServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()
