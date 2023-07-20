from andyamo import types

from pydantic import BaseModel, Field

class Message(BaseModel):
    message: str

class Point(BaseModel):
    lon: float
    lat: float

    class Config:
        schema_extra = {
            "example": {
                "lon": 3.127781750469675,
                "lat": 45.76400009445323
            }
        }


class LineString(BaseModel):
    type: str
    coordinates: list[list[float]]

    
class RouteRequest(BaseModel):
    start: Point = Field(..., description="The starting point for which the route should be calculated.")
    end: Point = Field(..., description="The ending point for which the route should be calculated.")
    profile: types.Profile = Field(..., description="See [availables profiles](#section/Routing-Profiles)")


class CoverageResponse(BaseModel):
    bbox: list[float] = Field(..., title="bbox", description="The bounding box of the geographical area covered. Format: [minLon,minLat,maxLon,maxLat]")

    class Config:
        schema_extra = {
            "example": {
                "bbox": [
                    3.073747158050537,
                    45.77367083508177,
                    3.075887560844421,
                    45.77517870042004
                ]
            }
        }    
    


class RouteResponsePath(BaseModel):
    distance: int = Field(..., description="Total distance in meters for the route returned")
    duration: int = Field(..., description="Estimated travel time in seconds. Depends on the chosen [profile](#section/Routing-Profiles)")
    points: LineString = Field(..., description="The geometry of the route in [GeoJSON format](https://datatracker.ietf.org/doc/html/rfc7946)")
    bbox: list[float] = Field(..., title="bbox", description="The bounding box of the route geometry. Format: [minLon,minLat,maxLon,maxLat]")
    segment_types: list[str] = Field(..., description="Segment types in the returned route result. Can be sidewalk, stair, crosswalk or unknown")

    class Config:
        schema_extra = {
            "example": {
                "distance": 280,
                "duration": 201,
                "points": {
                    "type": "LineString",
                    "coordinates": [
                        [
                            3.073747158050537,
                            45.77517870042004
                        ],
                        [
                            3.0739670991897583,
                            45.77472597094132
                        ],
                        [
                            3.0742889642715454,
                            45.77413105636887
                        ],
                        [
                            3.0747556686401367,
                            45.77379056781466
                        ],
                        [
                            3.074975609779358,
                            45.77367083508177
                        ],
                        [
                            3.0753082036972046,
                            45.77374940971673
                        ],
                        [
                            3.0754369497299194,
                            45.77386540064218
                        ],
                        [
                            3.0756354331970215,
                            45.77381301767344
                        ],
                        [
                            3.075887560844421,
                            45.773872883919395
                        ]
                    ]
                },
                "segment_types": ["sidewalk", "sidewalk", "crosswalk", "sidewalk", "sidewalk", "stair", "sidewalk", "sidewalk"],
                "bbox": [3.073747158050537, 45.77367083508177, 3.075887560844421, 45.77517870042004]
            }
        }
    
class PolygonGeometry(BaseModel):
    type: str
    coordinates: list[list[list[float]]]
    
    class Config:
        schema_extra = {
            "example": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            3.4716796874999996,
                            47.37603463349758
                        ],
                        [
                            3.49639892578125,
                            47.33603074146188
                        ],
                        [
                            3.6488342285156246,
                            47.429945332976125
                        ],
                        [
                            3.4716796874999996,
                            47.37603463349758
                        ]
                    ]
                ]
            }
        }
        
class Polygon(BaseModel):
    type: str
    properties: dict
    geometry: PolygonGeometry

    class Config:
        schema_extra = {
            "example": {
                "type": "Feature",
                "properties": {},
                "geometry": {
                    "type": "Polygon",
                    "coordinates": [
                        [
                            [
                                3.4716796874999996,
                                47.37603463349758
                            ],
                            [
                                3.49639892578125,
                                47.33603074146188
                            ],
                            [
                                3.6488342285156246,
                                47.429945332976125
                            ],
                            [
                                3.4716796874999996,
                                47.37603463349758
                            ]
                        ]
                    ]
                }
            }
        }

