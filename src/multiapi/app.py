from typing import Optional

from fastapi import FastAPI
import uvicorn

from utils import setup_logging

setup_logging()

app = FastAPI()


@app.get("/health")
async def health():
    """Used by Docker to check the health of the service"""
    return "OK"


@app.get("/life_expectancy/{sex}/{race}/{year}")
async def life_expectancy(sex: str, race: str, year: int):
    pass


@app.get("/unemployment/{state}")
async def unemployment_rate(state: str):
    pass


@app.get("/trends")
async def historical_interest(phrase: str, start_date: Optional[str] = None, end_date: Optional[str] = None):
    pass


@app.get("/trends_weather")
async def weather_interest_for_last_7_days(phrase: str):
    pass


@app.get("/weather")
async def weather_for_last_7_days():
    pass


if __name__ == '__main__':
    uvicorn.run("app", host="127.0.0.1", port=8080, log_level="info")
