from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup_openapi(app: FastAPI):
    def app_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Fortris Technical Interview App",
            version="0.1.0",
            description="An OpenAPI schema to fetch data from multiple services",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://www.fortris.com/wp-content/uploads/2021/07/fortris-logo.svg"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return app_openapi
