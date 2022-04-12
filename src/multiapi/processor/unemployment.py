import httpx
from lxml import html

from model import UnemploymentRate, USState, AppException

from .base import BaseProcessor


class UnemploymentProcessor(BaseProcessor[UnemploymentRate]):
    
    def __init__(self, url: str):
        self.url = url
        self.store: dict = {}
        self.current_month = None  # TODO: Introduce logic to update this every month

    def get(self, value: USState) -> UnemploymentRate:
        current_rate = self.store.get(USState.name(value))

        if current_rate is not None:
            return UnemploymentRate(current_rate)
        else:
            raise AppException(f"Unable to retrieve unemployment rate for state {value}")

    def parse(self) -> dict[str, float]:
        """Extracts and parses data from the given URL"""
        response = httpx.get(self.url)
        response.raise_for_status()

        try:
            rates, table = {}, html.fromstring(response.text).get_element_by_id("lauhsthl")

            self.current_month, *_ = table.find("thead/tr/th[2]").text.split(" ")

            for row in table.find("tbody").getchildren():
                state_name, last_month_rate = row.find("th/p").text, row.find("td[1]/span").text
                rates[state_name] = last_month_rate

            return rates
        except Exception as e:
            raise AppException(f"Unable to parse unemployment rate table: {str(e)}")


