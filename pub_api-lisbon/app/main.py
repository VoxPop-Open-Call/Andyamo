import sys
import json
import time
import hashlib
from fastapi import FastAPI, Body
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import requests
from .config import settings

import numpy as np
from scipy.spatial import KDTree
from scipy.spatial import ConvexHull

import grpc
from . import route_service_pb2 
from . route_service_pb2_grpc import RouteServiceStub
from .schemas import (
    Message,
    Point,
    LineString,
    Polygon,
    PolygonGeometry,
    RouteRequest,
    CoverageResponse,
    RouteResponsePath
)

from andyamo import types

from geopy import distance as geo_distance

from fastapi.encoders import jsonable_encoder
from fastapi.openapi.utils import get_openapi

from fastapi import Security, Depends, FastAPI, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from starlette.status import HTTP_403_FORBIDDEN
from starlette.responses import RedirectResponse, JSONResponse

channel = grpc.insecure_channel(f"{settings.grpc_server_host}:{settings.grpc_server_port}")
grpc_client = RouteServiceStub(channel)



def get_hash(data: str):
    return hashlib.md5(f"{data}".encode("utf-8")).hexdigest()

with open("export_clean_splitted.json", "r") as f:
    data = [json.loads(x.strip()) for x in f.readlines()]

hash_to_type = {}

for feature in data:
    hash_to_type[feature["feature"]["properties"]["index"]] = feature["feature"]["properties"]["type"]

    

datastore = {}

for _profile in ["foot", "manual_wheelchair", "electric_wheelchair"]:
    datastore[_profile] = {}
    datastore[_profile]["points"] = []
    datastore[_profile]["ids"] = []

    req_data = {"profile": types.Profile(_profile).name}
    request = route_service_pb2.Profile(**req_data)

    for node in grpc_client.ListNodes(request):
        #print(node.index, node.longitude, node.latitude)
        datastore[_profile]["points"].append([node.longitude, node.latitude])
        datastore[_profile]["ids"].append(node.index)

    datastore[_profile]["kdtree"] = KDTree(datastore[_profile]["points"])

nodeid_to_coords = {}
for feature in data:
    nodeid_to_coords["d_" + feature['feature']["properties"]["nodes"][0]] = \
        feature['feature']["geometry"]['coordinates'][0]
    nodeid_to_coords["d_" + feature['feature']["properties"]["nodes"][1]] = \
        feature['feature']["geometry"]['coordinates'][1]
    
def compute_convex_hull():
    _points = np.array(datastore["foot"]["points"])
    hull = ConvexHull(_points)

    hull_geojson = {
        "type": "Feature",
        "properties": {},
        "geometry": {
            "type": "Polygon",
            "coordinates": [
            ]
        }
    }

    l = []
    for vertex in hull.vertices: 
        l.append(list(datastore["foot"]["points"][vertex]))

    l.append(list(datastore["foot"]["points"][hull.vertices[0]]))
    hull_geojson["geometry"]["coordinates"] = [l]

    return hull_geojson

hull_geojson = compute_convex_hull()

    
def compute_coverage(features: list) -> tuple:
    """Return bounding box of the geographical area covered by this instance."""

    min_lon = sys.maxsize
    min_lat = sys.maxsize
    max_lon = 0
    max_lat = 0
    
    for feature in data:
        for (lon, lat) in feature["feature"]["geometry"]["coordinates"]:
            if lon < min_lon:
                min_lon = lon
            if lon > max_lon:
                max_lon = lon
    
            if lat < min_lat:
                min_lat = lat
            if lat > max_lat:
                max_lat = lat
    
            
    return min_lon,min_lat,max_lon,max_lat

    
def get_point_from_nodeid(nodeid):
    return nodeid_to_coords[nodeid]
        
app = FastAPI()


class ConvexHullResponse(BaseModel):
    polygon: Polygon = Field(..., title="polygon", description="Similar to /coverage, returns the convex hull corresponding to the geographical area covered as a GeoJSON polygon.")

        

@app.get("/healthz", summary="Check if API is up or not")
def healthz():
    return { "healthy": "OK" }

    
@app.get("/coverage", summary="Coverage information (bounding box)", response_model=CoverageResponse)
def coverage():
    bbox = compute_coverage(data)
    return { "bbox": bbox }


@app.get("/convex", summary="Coverage information (convex hull)", response_model=ConvexHullResponse)
def coverage():
    return { "polygon": hull_geojson }


@app.post(
    "/route",
    summary="Pedestrian routing",
    response_model=RouteResponsePath,
    responses={
        400: {"model": Message},
        404: {"model": Message}
    }
)
def route(route: RouteRequest = Body(...)) -> RouteResponsePath:


    if route.profile.value not in ["foot", "manual_wheelchair", "electric_wheelchair"]:
        return JSONResponse(
            status_code=404, content={
                "message": "Profile not available yet. Available profiles are: foot, manual_wheelchair and electric_wheelchair"
            }
        )
    

    _, idx_start = datastore[route.profile.value]["kdtree"]\
        .query([route.start.lon, route.start.lat])
    _, idx_end = datastore[route.profile.value]["kdtree"]\
        .query([route.end.lon, route.end.lat])

    too_far_from_graph = False
    
    if geo_distance.distance(
            get_point_from_nodeid(str(datastore[route.profile.value]["ids"][idx_start])[1:]),
            [route.start.lon, route.start.lat]
    ).m > settings.closest_point_tolerance:
        too_far_from_graph = True

    if geo_distance.distance(
            get_point_from_nodeid(str(datastore[route.profile.value]["ids"][idx_end])[1:]),
            [route.end.lon, route.end.lat]
    ).m > settings.closest_point_tolerance:
        too_far_from_graph = True

    if too_far_from_graph:
    
        return JSONResponse(
            status_code=400, content={
                "message": "Start and or end point outside covered perimeter"
            }
        )

    
    req_data = {
        "start": str(datastore[route.profile.value]["ids"][idx_start]),
        "end": str(datastore[route.profile.value]["ids"][idx_end]),
        "profile": route_service_pb2.Profile(profile=route.profile.name)
    }

        
    request = route_service_pb2.RouteRequest(**req_data)
    response = grpc_client.ShortestPath(request)
    route = response.route
    distance = response.distance
    
    if distance > settings.max_route_length_allowed:
        return JSONResponse(status_code=404, content={"message": "No route found."})
  
    route_points = [get_point_from_nodeid(x[1:]) for x in route]

    segment_types = []

    for i in range(len(route_points) - 1):
        segment_hash0 = get_hash([route_points[i], route_points[i+1]])
        segment_hash1 = get_hash([route_points[i+1], route_points[i]])

        if segment_hash0 in hash_to_type.keys():
            segment_types.append(hash_to_type[segment_hash0])
        elif segment_hash1 in hash_to_type.keys():
            segment_types.append(hash_to_type[segment_hash1])
                    
        if len(segment_types) < i+1:
            segment_types.append("unknown")


    min_lon = min([x[0] for x in route_points])
    min_lat = min([x[1] for x in route_points])
    max_lon = max([x[0] for x in route_points])
    max_lat = max([x[1] for x in route_points])

    walking_speed = 4000 / 3600 ## 4km/h == 4000 / 3600 m / s
    return {
        "distance": distance,
        "duration": distance * walking_speed,
        "points": {
            "type": "LineString",
            "coordinates": route_points
        },
        "segment_types": segment_types,
        "bbox": [min_lon, min_lat, max_lon, max_lat]

        }
    
    
    return JSONResponse(status_code=404, content={"message": "No route found."})

