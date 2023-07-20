import json
import random
from copy import deepcopy
from collections import namedtuple

import access
from andyamo import types

from generator import generate_graph
from geopy import distance as geo_distance


Edge = namedtuple("Edge", ["start_id", "end_id", "distance"])

with open("data.json", "r") as f:
    data = [json.loads(x.strip()) for x in f.readlines()]
    

def get_graph(profile: types.Profile):
    node_set = set()
    edges = list()

    for feature in data:
        try:
            if access.is_accessible(feature, profile):
                nodes = feature["feature"]["properties"]["nodes"]
                if len(nodes) == 2:
                    coordinates = feature["feature"]["geometry"]["coordinates"]
            
                    for node in nodes:
                        node_set.add(f"id_{node}")
    
                    distance = 0
                    for i in range(len(coordinates)-1):
                        distance += geo_distance.distance(
                            coordinates[i], coordinates[i+1]
                        ).m
                        
                    edges.append(Edge(f"id_{nodes[0]}", f"id_{nodes[1]}", distance))
    
    
        except Exception as e :
            print(feature)
            raise(e)
            
    node_ids = list(node_set)
    return node_ids, edges


node_ids, edges = get_graph(types.Profile("manual_wheelchair"))
generate_graph("manual_wheelchair.cpp", "c_manual_wheelchair", node_ids, edges)

node_ids, edges = get_graph(types.Profile("electric_wheelchair"))
generate_graph("electric_wheelchair.cpp", "c_electric_wheelchair", node_ids, edges)

node_ids, edges = get_graph(types.Profile("foot"))
generate_graph("foot.cpp", "c_foot", node_ids, edges)
