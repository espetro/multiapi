import httpx

from model import LifeExpectancy, SexType, RaceType
from .base import AsyncBaseProcessor


class LifeExpectancyProcessor(AsyncBaseProcessor[LifeExpectancy]):

    def __init__(self, url: str):
        self.url = url
        self.client = httpx.AsyncClient()

    async def async_teardown(self):
        await self.client.aclose()

    async def get(self, sex: SexType, race: RaceType, year: int) -> LifeExpectancy:
        query_parameters = {
            "sex": sex.name,
            "race": race.name,
            "year": year
        }

        response = await self.client.get(self.url, params=query_parameters)
        response.raise_for_status()

        data = response.json()
        return LifeExpectancy(data["average_life_expectancy"])
