import httpx
from lxml.etree import HTML

from model import UnemploymentRate, USState, AppException

from .base import BaseProcessor


class UnemploymentProcessor(BaseProcessor[UnemploymentRate]):
    
    def __init__(self, url: str):
        self.url = url
        self.store: dict = {}
        self.current_month = None

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

        rates, table = {}, HTML(response.text).find('body/table[@id="lauhsthl"]')

        if table is not None:
            self.current_month = table.find('thead/tr[@id="lauhsthl-0-1"]')
            for row in table.findAll('tbody/tr'):
                state_name, last_month_rate, *_ = list(row.findAll('td'))
                rates[state_name] = last_month_rate
        else:
            raise AppException("Unable to parse unemployment rate table: cannot find data table")

        return rates

