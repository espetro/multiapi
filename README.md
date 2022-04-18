
# Multi API

This is a sample REST API project written in Python which features:

- A fully asynchronous API, using FastAPI. There are both async and sync endpoints.
- A set of unit, integration, and load tests to ensure the API works and performs as expected.
- An OpenAPI schema, so that it's simpler to test the endpoints manually, and to generate clients. 
- A dockerized version of the API along with a deployment configuration in `docker-compose.yaml`.

## Requirements

- Python 3.10
- Docker
- Make
- A `.env` file in the root directory, with the following keys:
  - `IP_REGISTRY_KEY` with the API key for https://ipregistry.co/
  - `WEATHER_API_KEY` with the API key for https://www.weatherapi.com/

As for the Python packages required, make sure to create a virtual environment and activate it, 
and then run `make install-requirements`. 

## How to run it

The simplest way to run it is with `make run`, which will run the application directly. 

You can also start it with `make docker-run`, which will build a Docker image and then run it. To stop it, you can do it
manually, or running `make docker-stop`.

## How to test it

### Manual tests

Once the application has started, go to http://localhost:8080/docs
(the default port is 8080, but you can change it in the Docker deployment).

### Unit tests

By running `make tests`.

### Integration tests

By running `make integration-tests`.