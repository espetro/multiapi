from datetime import datetime, timedelta

from lxml import etree
import httpx
from ipregistry import IpregistryClient

from model import Weather, WeatherDay
from .base import AsyncBaseProcessor


class WeatherProcessor(AsyncBaseProcessor[Weather]):

    ENDPOINT = "/history.xml"

    def __init__(self, url: str, ip_registry_key: str, weather_api_key: str):
        self.url = url
        self.client = httpx.AsyncClient(base_url=url)

        self.ip_registry = IpregistryClient(ip_registry_key)
        self.weather_api_key = weather_api_key

    async def async_teardown(self):
        await self.client.aclose()

    async def get(self, client_ip: str, start_date: datetime = datetime.now()) -> Weather:
        weather_data, location = [], self.lookup(client_ip)

        for date in [start_date - timedelta(days=n) for n in range(7)]:
            date_str = date.strftime("%Y-%m-%d")
            query_parameters = {
                "key": self.weather_api_key,
                "q": location,
                "dt": date_str
            }

            response = await self.client.get(self.ENDPOINT, params=query_parameters)
            response.raise_for_status()

            day_data = self.parse(date_str, response.content)
            weather_data.append(day_data)

        return Weather(weather_data)

    def lookup(self, client_ip: str) -> str:
        ip_info = self.ip_registry.lookup(client_ip)
        return f"{ip_info.location['latitude']},{ip_info.location['longitude']}"

    @staticmethod
    def parse(date: str, xml_input: bytes) -> WeatherDay:
        root = etree.fromstring(xml_input)
        day_data = root.find("forecast/forecastday/day")
        astro_data = root.find("forecast/forecastday/astro")

        return WeatherDay(
            date,
            float(day_data.find("maxtemp_c").text),
            float(day_data.find("mintemp_c").text),
            float(day_data.find("avgtemp_c").text),
            float(day_data.find("maxwind_kph").text),
            float(day_data.find("totalprecip_mm").text),
            float(day_data.find("avghumidity").text),
            day_data.find("condition/text").text,
            int(day_data.find("uv").text),
            astro_data.find("sunrise").text,
            astro_data.find("sunset").text,
        )

