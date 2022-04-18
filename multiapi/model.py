from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

import us.states
from phantom import Phantom
from phantom.schema import Schema


def _is_a_us_state(value: str) -> bool:
    """Checks if a string is a valid US state alpha code. Examples: FL, NY, MA"""
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
    def of(value: str) -> str:
        return us.states.lookup(value).name


@dataclass
class LifeExpectancy:
    average_life_expectancy: float


@dataclass
class UnemploymentRate:
    rate: float


@dataclass
class PhraseTrendDay:
    date: str
    interest: float


@dataclass
class PhraseTrends:
    trends: list[PhraseTrendDay]

    def to_json(self):
        return {"interest": [_.interest for _ in self.trends]}


@dataclass
class WeatherDay:
    date: str
    max_temperature_celsius: float
    min_temperature_celsius: float
    avg_temperature_celsius: float
    max_wind_speed_kph: float
    total_precipitations_mm: float
    avg_humidity: float
    forecast_text: str
    uv_index: int
    sunrise: str
    sunset: str

    def to_json(self):
        return {
            "date": self.date,
            "max. temperature": f"{self.max_temperature_celsius} °C",
            "min. temperature": f"{self.min_temperature_celsius} °C",
            "average temperature": f"{self.avg_temperature_celsius} °C",
            "max. wind speed": f"{self.max_wind_speed_kph} km/h",
            "rainfall": f"{self.total_precipitations_mm} mm",
            "humidity": f"{self.avg_humidity}%",
            "forecast": self.forecast_text,
            "UV index": self.uv_index,
            "sunrise": self.sunrise,
            "sunset": self.sunset
        }


@dataclass
class Weather:
    dates: list[WeatherDay]

    def items(self) -> list:
        """Returns a list of weather data for each day"""
        return [date.to_json() for date in self.dates]


@dataclass
class TrendsAndWeather:
    weather: Weather
    interests: PhraseTrends

    def to_json(self) -> list:
        result = []
        for (interests, weather_data) in zip(self.interests.trends, self.weather.items()):
            date = weather_data.pop("date")
            result.append({"date": date, "interest": interests.interest, "weather": weather_data})

        return result


@dataclass
class AppException(Exception):
    message: str
    status: int = 400
