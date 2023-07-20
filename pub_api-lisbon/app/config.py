from pydantic import BaseSettings

class Settings(BaseSettings):
    grpc_server_host: str = "127.0.0.1"
    grpc_server_port: str = "50051"

    # Defines the maximum allowed distance in meters
    # of a route. Above this threshold, a 404 response code
    # will be returned meaning no route correspond to the request.
    max_route_length_allowed: int = 20000

    # Maximum allowed distance in meters between a requested route
    # start/end point and the closest point on our graph 
    closest_point_tolerance: int = 150
    
    class Config:
        env_file = ".env"
    
# reads env variables (case insensitive) and validate against schema
settings = Settings()
