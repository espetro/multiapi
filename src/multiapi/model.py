from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum

import us.states
from phantom import Phantom
from phantom.schema import Schema


def _is_a_us_state(value: str) -> bool:
    if len(value) == 2:
        try:
            return us.states.lookup(value) is not None
        except:
            pass
    return False


class SexType(str, Enum):
    male = "male"
    female = "female"
    both_sexes = "both-sexes"

    @property
    def name(self):
        return " ".join(_.capitalize() for _ in self.value.split("-"))


class RaceType(str, Enum):
    """These groups are mutually exclusive"""
    white = "white"
    black = "black"
    all_races = "all-races"

    @property
    def name(self):
        return " ".join(_.capitalize() for _ in self.value.split("-"))


class USState(str, Phantom, predicate=_is_a_us_state):
    """A narrowed string for representing US state abbreviations"""

    @classmethod
    def __schema__(cls) -> Schema:
        return super().__schema__() | Schema(
            description="A type for US states",
            format="custom-name",
        )

    @staticmethod
    def name(state: USState) -> str:
        return us.states.lookup(state)


@dataclass
class LifeExpectancy:
    average_life_expectancy: float


@dataclass
class UnemploymentRate:
    rate: float


@dataclass
class PhraseTrends:
    interest: list[float]


@dataclass
class Weather:
    dates: list[datetime]
    max_temperature: list[float]
    # TODO

    def items(self) -> list:
        """Returns a list of weather data for each day"""
        return [{"date": date} for (date) in self.dates]  # TODO


@dataclass
class TrendsAndWeather:
    weather: Weather
    interests: PhraseTrends

    def to_json(self) -> list:
        return [{"date": weather["date"], "interest": interest, "weather": weather["data"]}
                for (interest, weather) in zip(self.interests.interest, self.weather.items())]


@dataclass
class AppException(Exception):
    message: str
    status: int = 400
