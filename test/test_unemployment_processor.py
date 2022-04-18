from importlib import resources

import respx
from httpx import Response

from model import UnemploymentRate
from processor import UnemploymentProcessor

SAMPLE_DATA = resources.read_text("test.resources", "unemployment.html")


@respx.mock
def test_get_unemployment_for_florida():
    url = "http://localhost"
    processor = UnemploymentProcessor(url, update_frequency=1)

    expected_response = Response(200, html=SAMPLE_DATA)
    _ = respx.get(url).mock(return_value=expected_response)

    result = processor.get("FL")
    assert result == UnemploymentRate(3.3)
