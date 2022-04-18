import respx
import pytest
from httpx import Response

from model import SexType, RaceType, LifeExpectancy
from processor import LifeExpectancyProcessor


def _build_url(base_url: str, sex: SexType, race: RaceType, year: int):
    return f"{base_url}{LifeExpectancyProcessor.ENDPOINT}?sex={sex.name}&race={race.name}&year={year}"


@respx.mock
@pytest.mark.asyncio
async def test_get_life_expectancy_for_white_men_in_1990():
    url = "http://localhost"
    processor = LifeExpectancyProcessor(url)
    sex, race, year = SexType.male, RaceType.white, 1990

    url = _build_url(url, sex, race, year)
    expected_response = Response(200, json=[{"average_life_expectancy": 70}])
    _ = respx.get(url).mock(return_value=expected_response)

    result = await processor.get(sex, race, year)
    assert result == LifeExpectancy(70)
