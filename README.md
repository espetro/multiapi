
# Multi API

This is a sample REST API project written in Python which features:

- A fully asynchronous API, using FastAPI. There are both async and sync endpoints.
- A set of unit and integration tests to ensure the API works and performs as expected.
- An OpenAPI schema, so that it's simpler to test the endpoints manually, and to generate clients. 
- A dockerized version of the API along with a deployment configuration in `docker-compose.yaml`.

## Requirements

- Python 3.10
- Docker
- Make
- A `.env` file in the root directory, with the following keys:
  - `IP_REGISTRY_KEY` with the API key for https://ipregistry.co/
  - `WEATHER_API_KEY` with the API key for https://www.weatherapi.com/

You can omit the `.env` file, but don't expect the _Weather_ endpoints to work if so.

As for the Python packages required, make sure to create a virtual environment and activate it, 
and then run `make install-requirements`. 

## How to run it

The simplest way to run it is with `make run`, which will run the application directly in your PC.
You can also run it in a Docker container with `make docker-run`, which will build a Docker image and then run it. To stop it, just close the terminal session or press CTRL+C.
If you want to deploy it with other services, which is usually done by using a Docker Compose file (`docker-compose.yaml`), then use `make docker-run-compose`.

Logging level can be set up via the environment variable `LOG_LEVEL`. The available log levels are listed in
https://docs.python.org/3/library/logging.html#logging-levels

## How to test it

### Manual tests

Once the application has started, go to http://localhost:80/docs
(the default port is 80, but you can change it).

### Unit tests

By running `make tests`.

### Integration tests

By running `make integration-tests`.

### Load tests

Load tests are performed manually by running `make run` and then `make load-tests`. Then, go to localhost:8089 and set
the following values:
  
- Number of users: 100
- Spawn rate: 5
- Host: http://localhost:8080
