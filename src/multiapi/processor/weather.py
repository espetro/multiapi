from datetime import datetime

import httpx
from ipregistry import IpregistryClient

from model import Weather
from .base import AsyncBaseProcessor


class WeatherProcessor(AsyncBaseProcessor[Weather]):

    def __init__(self, url: str):
        self.url = url
        self.ip_registry = IpregistryClient("1qanqdhes62xy30u")
        self.client = httpx.AsyncClient()

    async def async_teardown(self):
        await self.client.aclose()

    async def get(self, client_ip: str) -> Weather:
        location = self.lookup(client_ip)
        today = datetime.now().strftime("%Y-%m-%d")
        query_parameters = {
            "key": "8922824f4009452591b104033221204",
            "q": location,
            "days": 7,
            "dt": today
        }

        response = await self.client.get("/history.xml", params=query_parameters)
        response.raise_for_status()

        return self.parse(response.text)

    def lookup(self, client_ip: str) -> str:
        ip_info = self.ip_registry.lookup(client_ip)
        return ip_info.location['city']

    @staticmethod
    def parse(xml_input: str) -> Weather:
        pass
