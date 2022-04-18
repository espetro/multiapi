from datetime import datetime

import responses
from pytrends.request import TrendReq

from model import PhraseTrends, PhraseTrendDay
from processor import TrendsProcessor


def _random_characters(length: int) -> str:
    return ')]}\')]}\''[:length]


def _build_token_response() -> str:
    return _random_characters(4) + '{"widgets":[]}'


def _build_raw_response() -> str:
    return _random_characters(5) + '{"default": {"timelineData": [{"time": "1640995200", "formattedTime": "Jan 1, ' \
                                   '2022", "formattedAxisTime": "Jan 1, 2022", "value": [100], "hasData": [true], ' \
                                   '"formattedValue": ["90"]}], "averages": []}} '


@responses.activate
def test_get_trends_for_a_single_day():
    start, end = datetime.strptime("2022-01-01", "%Y-%m-%d"), datetime.strptime("2022-01-01", "%Y-%m-%d")
    raw_token_response = _build_token_response()
    raw_response = _build_raw_response()
    phrase = "bitcoin"

    responses.add(responses.GET, "https://trends.google.com/?geo=US", status=200)

    api = TrendReq()
    processor = TrendsProcessor(api)

    api.interest_over_time_widget = {"request": '{}', "token": ""}

    responses.add(responses.GET, TrendReq.GENERAL_URL,
                  status=200, body=raw_token_response, content_type="application/json")

    responses.add(responses.GET, TrendReq.INTEREST_OVER_TIME_URL, status=200,
                  body=raw_response, content_type="application/json")

    result = processor.get(phrase, start, end)
    assert result == PhraseTrends([PhraseTrendDay('2022-01-01', 100)])
