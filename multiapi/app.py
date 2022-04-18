import logging
from typing import Optional
from datetime import date, datetime, timedelta

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
async def health_handler():
    """Used by Docker to check the health of the service"""
    return "OK"


@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy_handler(sex: SexType, race: RaceType, year: int):
    logging.info(f"Retrieving life expectancy for {race} {sex} in {year}")
    result = await life_expectancy.get(sex, race, year)
    return result


@app.get("/unemployment/{state}")
def unemployment_rate_handler(state: USState):
    state_name = USState.of(state)
    logging.info(f"Retrieving unemployment rate in {state_name} (last updated in {unemployment.last_update_date})")
    return unemployment.get(state)


@app.get("/trends")
def trends_interest_handler(phrase: str, start_date: Optional[date] = None, end_date: Optional[date] = None):
    """
    :param phrase: A sentence to look into Google Trends
    :param start_date: A date with the format YYYY-mm-dd
    :param end_date: A date with the format YYYY-mm-dd
    """
    logging.info(f"Retrieving interest for {phrase} in the last 7 days")

    if start_date is None or end_date is None:
        _end_date = datetime.now()
        return trends.get(phrase, _end_date - timedelta(weeks=2), _end_date).to_json()
    else:
        return trends.get(phrase, start_date, end_date).to_json()


@app.get("/trends_weather")
async def weather_and_trends_for_last_7_days_handler(phrase: str, request: Request):
    logging.info(f"Retrieving weather and interest for {phrase} in the last 7 days")

    _end_date = datetime.now()
    client_ip = get_client_ip(request)

    trends_result = trends.get(phrase, _end_date - timedelta(weeks=1), _end_date)
    weather_result = await weather.get(client_ip)
    return TrendsAndWeather(weather_result, trends_result).to_json()


@app.get("/weather")
async def weather_for_last_7_days_handler(request: Request):
    logging.info(f"Retrieving weather data for the last 7 days")

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
