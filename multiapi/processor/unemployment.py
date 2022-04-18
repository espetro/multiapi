import re
from datetime import datetime

import httpx
from lxml import html

from model import UnemploymentRate, USState, AppException

from .base import BaseProcessor


class UnemploymentProcessor(BaseProcessor[UnemploymentRate]):
    
    def __init__(self, url: str, update_frequency: int = 1):
        """
        :param url: The website URL from where to extract unemployment data
        :param update_frequency: The number of days to wait until the store is updated
        """
        self.url = url
        self.store: dict[str, float] = {}

        self.last_update_date = datetime.strptime("1990-01-01", "%Y-%m-%d")
        self.update_frequency = update_frequency

    def get(self, value: USState) -> UnemploymentRate:
        self.check_if_update_is_required()
        current_rate = self.store.get(USState.of(value))

        if current_rate is not None:
            return UnemploymentRate(current_rate)
        else:
            raise AppException(f"Unable to retrieve unemployment rate for state {value}")

    def parse(self) -> dict[str, float]:
        """Extracts and parses data from the given URL"""
        response = httpx.get(self.url)
        response.raise_for_status()

        try:
            rates, tree = {}, html.fromstring(response.text)
            table = tree.get_element_by_id("lauhsthl")

            self.last_update_date = self.get_update_date(tree)

            for row in table.find("tbody").getchildren():
                state_name, last_month_rate = row.find("th/p").text, row.find("td[1]/span").text
                rates[state_name] = float(last_month_rate)

            return rates
        except Exception as e:
            raise AppException(f"Unable to parse unemployment rate table: {str(e)}")

    def check_if_update_is_required(self):
        """Checks if the store needs to be updated"""
        if (datetime.now() - self.last_update_date).days >= self.update_frequency:
            self.store = self.parse()

    @staticmethod
    def get_update_date(tree: html.HtmlElement) -> datetime:
        update_tag, *_ = tree.xpath("//p[@class='update']")
        *_, raw_date = update_tag.itertext()
        formatted_date = " ".join(re.findall(r"\w+", raw_date))

        return datetime.strptime(formatted_date, "%B %d %Y")


