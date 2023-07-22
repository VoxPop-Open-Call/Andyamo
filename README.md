# Andyano Routing Service 

The Andyamo Routing Service is a microservices-based application composed of two main components: a Web API and a gRPC API. This service provides efficient and flexible **pedestrian** routing capabilities, allowing clients to plan and optimize routes for various purposes and mobility level.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Installation](#installation)
- [License](#license)

## Introduction

provides efficient and flexible pedestrian route planning capabilities, catering to different mobility profiles, including manual wheelchair and electric wheelchair users.

## Features

- **Web API**: The Web API provides RESTful endpoints to interact with the Routing Service. Clients can submit route requests and receive optimized routes in response.

- **gRPC API**: The gRPC API is used by the Web API for backend calculations. It allows efficient communication between the microservices using Google's Protocol Buffers (protobuf) and provides improved performance over traditional REST APIs.

- **Route Optimization**: The service utilizes advanced algorithms to optimize routes based on factors like distance, terrain constraints, and client preferences.

- **Scalability**: The microservices architecture ensures that the Routing Service can handle a large number of requests and distribute the workload effectively.

## Architecture

The Routing Service follows a microservices architecture, comprising two main components:

1. **Web API**: This component serves as the entry point for clients. It accepts incoming RESTful requests from external applications and forwards them to the gRPC API for route calculation. It then returns the optimized routes back to the clients.

2. **gRPC API**: The gRPC API is responsible for route calculations and optimization. It receives requests from the Web API and processes them using efficient algorithms. The optimized route data is returned to the Web API for further delivery to clients.

The use of gRPC for communication between the two services improves performance and reduces latency, making the Routing Service highly responsive and suitable for real-time applications.

## Installation

To set up the Routing Service, follow these steps:

1. Clone the repository
2. Navigate to the project directory: `cd routing-service`
3. Run the services using docker compose:
   ```
   docker compose build
   ```
   
## Usage

To start the Routing Service, run the following command:

```
   docker compose up -d
```

The Routing Service will now be running, and you can start making requests to the API.
See [local documentation](http://localhost:8066/) for the complete list of endpoints and route parameters.


## License

The Routing Service is licensed under the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html#license-text). Feel free to use, modify, and distribute the service as per the terms of the license.

---
This README provides an overview of the Routing Service and how to use it effectively. For more detailed information on endpoints, request payloads, and response formats, refer to the API documentation included with the codebase and accessible at http://localhost:8066.
=======


