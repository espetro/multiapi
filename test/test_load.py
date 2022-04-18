import random
from datetime import date

import us
from locust import HttpUser, task, between

from multiapi.model import SexType, RaceType

STATES_SHORTCODES = [_.abbr for _ in us.STATES]


def random_sex() -> str:
    return random.choice(list(SexType)).value


def random_race() -> str:
    return random.choice(list(RaceType)).value


def random_year() -> int:
    return random.choice(range(1940, 2000))


def random_state() -> str:
    return random.choice(STATES_SHORTCODES)


def random_date_range() -> (date, date):
    reference_start_date, reference_end_date = date(2021, 1, 1).toordinal(), date(2021, 1, 31).toordinal()
    random_start_date = random.randint(reference_start_date, reference_end_date - 1)
    random_end_date = reference_start_date

    while random_end_date < random_start_date:
        random_end_date = random.randint(reference_start_date, reference_end_date)

    return date.fromordinal(random_start_date), date.fromordinal(random_end_date)


class TestLoadUser(HttpUser):
    wait_time = between(1, 10)

    @task(2)
    def test_life_expectancy(self):
        self.client.get(f"/life_expectancy/{random_sex()}/{random_race()}/{random_year()}")

    @task(2)
    def test_unemployment_rate(self):
        self.client.get(f"/unemployment/{random_state()}")

    @task(1)
    def test_weather_last_week(self):
        self.client.get("/weather")

    @task(1)
    def test_weather_and_trends_last_week(self):
        self.client.get("/trends_weather", params={"phrase": "illo"})

    @task(2)
    def test_trends(self):
        start_date, end_date = random_date_range()
        self.client.get("/trends", params={"phrase": "illo", "start_date": start_date, "end_date": end_date})
