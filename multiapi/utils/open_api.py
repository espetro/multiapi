from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


def setup_openapi(app: FastAPI):
    def app_openapi():
        if app.openapi_schema:
            return app.openapi_schema

        openapi_schema = get_openapi(
            title="Rocket App",
            version="0.1.0",
            description="An OpenAPI schema to fetch data from multiple services",
            routes=app.routes,
        )
        openapi_schema["info"]["x-logo"] = {
            "url": "https://cdn.icon-icons.com/icons2/1234/PNG/512/1492719123-rocket_83625.png"
        }
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    return app_openapi
