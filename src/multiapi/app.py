from typing import Optional
from datetime import datetime, timedelta

from fastapi import FastAPI
import uvicorn
from fastapi.responses import JSONResponse
from fastapi import Request

from utils import setup_logging
from model import SexType, RaceType, USState, AppException, TrendsAndWeather
from processor import UnemploymentProcessor, LifeExpectancyProcessor, TrendsProcessor, WeatherProcessor

setup_logging()

unemployment = UnemploymentProcessor("https://www.bls.gov/web/laus/lauhsthl.htm")
life_expectancy = LifeExpectancyProcessor("https://data.cdc.gov/resource/w9j2-ggv5.json")
trends = TrendsProcessor("")
weather = WeatherProcessor("https://www.weatherapi.com/docs/#")

app = FastAPI()


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
def trends_interest(phrase: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    if start_date is None or end_date is None:
        _end_date = datetime.now()
        return trends.get(phrase, _end_date - timedelta(weeks=2), _end_date)
    else:
        return trends.get(phrase, start_date, end_date)


@app.get("/trends_weather")
async def weather_and_trends_for_last_7_days(phrase: str, request: Request):
    _end_date = datetime.now()
    trends_result = trends.get(phrase, _end_date - timedelta(weeks=1), _end_date)
    weather_result = await weather.get(request.client.host)

    return TrendsAndWeather(weather_result, trends_result).to_json()


@app.get("/weather")
async def weather_for_last_7_days(request: Request):
    response = await weather.get(request.client.host)
    return response.items()


@app.exception_handler(AppException)
async def app_exception_handler(_: Request, exc: AppException):
    return JSONResponse(status_code=exc.status, content={"message": exc.message})


@app.on_event("shutdown")
async def on_shutdown():
    await weather.async_teardown()
    await life_expectancy.async_teardown()


if __name__ == '__main__':
    uvicorn.run("app", host="127.0.0.1", port=8080, log_level="info")