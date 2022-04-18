from typing import Optional
from datetime import date, datetime, timedelta

import uvicorn
from decouple import config
from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse

from utils import setup_logging, setup_openapi
from model import SexType, RaceType, USState, AppException, TrendsAndWeather
from processor import UnemploymentProcessor, LifeExpectancyProcessor, TrendsProcessor, WeatherProcessor

setup_logging()

weather = WeatherProcessor("http://api.weatherapi.com/v1", config("IP_REGISTRY_KEY"), config("WEATHER_API_KEY"))
unemployment = UnemploymentProcessor("https://www.bls.gov/web/laus/lauhsthl.htm")
trends = TrendsProcessor()
life_expectancy = LifeExpectancyProcessor("https://data.cdc.gov")

app = FastAPI()
app.openapi = setup_openapi(app)


def get_client_ip(request: Request) -> str:
    """Retrieves the client IP from the request. If the IP is a loopback address, then return an empty string"""
    return "" if request.client.host == "127.0.0.1" else request.client.host


@app.get("/health")
async def health():
    """Used by Docker to check the health of the service"""
    return "OK"


@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy(sex: SexType, race: RaceType, year: int):
    return await life_expectancy.get(sex, race, year)


@app.get("/unemployment/{state}")
def unemployment_rate(state: USState):
    return unemployment.get(state)


@app.get("/trends")
def trends_interest(phrase: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
    if start_date is None or end_date is None:
        _end_date = datetime.now()
        return trends.get(phrase, _end_date - timedelta(weeks=2), _end_date).to_json()
    else:
        return trends.get(phrase, start_date, end_date).to_json()


@app.get("/trends_weather")
async def weather_and_trends_for_last_7_days(phrase: str, request: Request):
    _end_date = datetime.now()
    client_ip = get_client_ip(request)

    trends_result = trends.get(phrase, _end_date - timedelta(weeks=1), _end_date)
    weather_result = await weather.get(client_ip)
    return TrendsAndWeather(weather_result, trends_result).to_json()


@app.get("/weather")
async def weather_for_last_7_days(request: Request):
    client_ip = get_client_ip(request)
    response = await weather.get(client_ip)
    return response.items()


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(status_code=exc.status, content={"message": exc.message})


@app.on_event("shutdown")
async def on_shutdown():
    await weather.async_teardown()
    await life_expectancy.async_teardown()


if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.1", port=8080, log_level="info")
