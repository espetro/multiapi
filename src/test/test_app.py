from httpx import AsyncClient
from unittest import IsolatedAsyncioTestCase
import respx

from app import app
from app.model import SexType, RaceType


class TestApp(IsolatedAsyncioTestCase):

    async def asyncSetUp(self) -> None:
        self.client = AsyncClient(app=app, base_url="localhost")

    async def asyncTearDown(self) -> None:
        await self.client.aclose()

    async def test_health(self):
        response = await self.client.get("/health")
        self.assertEqual(response.text, "OK")

    async def test_life_expectancy(self):
        response = await self.client.get(f"life_expectancy/{SexType.female}/{RaceType.white}/1998")
        self.assertEqual(response.json(), {"average_life_expectancy": 83})

    async def test_unemployment_rate(self):
        response = await self.client.get("unemployment/ny")
        self.assertEqual(response.json(), {"average_life_expectancy": 83})

    async def test_trends_interest(self):
        # TODO: Mock Google Trends service
        query_parameters = {"phrase": "easter-egg"}

        response = await self.client.get("trends", params=query_parameters)
        self.assertEqual(response.json(), {"interest": [0, 0, 0]})

    async def test_trends_interest_with_date_range(self):
        query_parameters = {
            "phrase": "roscon-de-reyes",
            "start_date": "2022-01-04",
            "end_date": "2022-01-06"
        }

        response = await self.client.get("trends", params=query_parameters)
        self.assertEqual(response.json(), {"interest": [0, 0, 0]})

    async def test_trends_interest_fails_without_phrase(self):
        response = await self.client.get("trends")
        self.assertEqual(response.status_code, 404)

    async def test_weather_and_trends_interest_for_last_7_days(self):
        query_parameters = {"phrase": "easter-egg"}
        expected_response = [
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}},
            {"date": "", "interest": 0, "weather": {}}
        ]

        response = await self.client.get("trends_weather", params=query_parameters)
        self.assertEqual(response.json(), expected_response)

    async def test_weather_and_trends_fails_without_phrase(self):
        response = await self.client.get("trends_weather")
        self.assertEqual(response.status_code, 404)

    async def test_weather_for_last_7_days(self):
        expected_response = [
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
            {"date": "", "weather": ""},
        ]

        response = await self.client.get("unemployment/ny")
        self.assertEqual(response.json(), expected_response)
