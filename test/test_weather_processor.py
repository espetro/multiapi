from datetime import datetime, timedelta
from importlib import resources

import pytest
import respx
from httpx import Response

from model import WeatherDay, Weather
from processor import WeatherProcessor

IP_SAMPLE = resources.read_text("test.resources", "ip_data.json")
DAY_0_XML = resources.read_binary("test.resources.weather", "day_0.xml")
DAY_1_XML = resources.read_binary("test.resources.weather", "day_1.xml")
DAY_2_XML = resources.read_binary("test.resources.weather", "day_2.xml")
DAY_3_XML = resources.read_binary("test.resources.weather", "day_3.xml")
DAY_4_XML = resources.read_binary("test.resources.weather", "day_4.xml")
DAY_5_XML = resources.read_binary("test.resources.weather", "day_5.xml")
DAY_6_XML = resources.read_binary("test.resources.weather", "day_6.xml")
ALL_DAYS_XML = [DAY_0_XML, DAY_1_XML, DAY_2_XML, DAY_3_XML, DAY_4_XML, DAY_5_XML, DAY_6_XML]


def _build_url(url: str, location: str, date: str):
    return f"{url}{WeatherProcessor.ENDPOINT}?key=&q={location}&dt={date}"


def test_xml_parse():
    date = "2022-04-13"
    expected_result = WeatherDay(
        date=date,
        max_temperature_celsius=17.7,
        min_temperature_celsius=11.7,
        avg_temperature_celsius=14.8,
        max_wind_speed_kph=11.2,
        total_precipitations_mm=0.7,
        avg_humidity=80.0,
        forecast_text='Light rain shower',
        uv_index=0,
        sunrise='07:29 AM',
        sunset='08:36 PM'
    )

    weather_data = WeatherProcessor.parse(date, DAY_0_XML)
    assert weather_data == expected_result


@respx.mock
@pytest.mark.asyncio
async def test_get_weather_info_for_last_7_days():
    expected_result = Weather([
        WeatherDay(date='2022-04-15',
                   max_temperature_celsius=17.7,
                   min_temperature_celsius=11.7,
                   avg_temperature_celsius=14.8,
                   max_wind_speed_kph=11.2,
                   total_precipitations_mm=0.7,
                   avg_humidity=80.0,
                   forecast_text='Light rain shower',
                   uv_index=0,
                   sunrise='07:29 AM',
                   sunset='08:36 PM'),
        WeatherDay(date='2022-04-14',
                   max_temperature_celsius=17.0,
                   min_temperature_celsius=10.4,
                   avg_temperature_celsius=14.7,
                   max_wind_speed_kph=20.5,
                   total_precipitations_mm=0.0,
                   avg_humidity=78.0,
                   forecast_text='Overcast',
                   uv_index=0,
                   sunrise='07:31 AM',
                   sunset='08:35 PM'),
        WeatherDay(date='2022-04-13',
                   max_temperature_celsius=17.3,
                   min_temperature_celsius=11.4,
                   avg_temperature_celsius=15.1,
                   max_wind_speed_kph=15.5,
                   total_precipitations_mm=0.0,
                   avg_humidity=79.0,
                   forecast_text='Overcast',
                   uv_index=0,
                   sunrise='07:32 AM',
                   sunset='08:34 PM'),
        WeatherDay(date='2022-04-12',
                   max_temperature_celsius=22.4,
                   min_temperature_celsius=13.0,
                   avg_temperature_celsius=18.4,
                   max_wind_speed_kph=26.6,
                   total_precipitations_mm=0.0,
                   avg_humidity=57.0,
                   forecast_text='Sunny',
                   uv_index=0,
                   sunrise='07:34 AM',
                   sunset='08:33 PM'),
        WeatherDay(date='2022-04-11',
                   max_temperature_celsius=25.0,
                   min_temperature_celsius=11.5,
                   avg_temperature_celsius=19.9,
                   max_wind_speed_kph=34.9,
                   total_precipitations_mm=0.0,
                   avg_humidity=44.0,
                   forecast_text='Partly cloudy',
                   uv_index=0,
                   sunrise='07:36 AM',
                   sunset='08:32 PM'),
        WeatherDay(date='2022-04-10',
                   max_temperature_celsius=26.7,
                   min_temperature_celsius=9.2,
                   avg_temperature_celsius=20.1,
                   max_wind_speed_kph=27.4,
                   total_precipitations_mm=0.0,
                   avg_humidity=50.0,
                   forecast_text='Sunny',
                   uv_index=0,
                   sunrise='07:37 AM',
                   sunset='08:31 PM'),
        WeatherDay(date='2022-04-09',
                   max_temperature_celsius=18.7,
                   min_temperature_celsius=7.7,
                   avg_temperature_celsius=14.2,
                   max_wind_speed_kph=20.2,
                   total_precipitations_mm=0.0,
                   avg_humidity=60.0,
                   forecast_text='Partly cloudy',
                   uv_index=0,
                   sunrise='07:39 AM',
                   sunset='08:30 PM')
    ])

    start_date = datetime.strptime("2022-04-15", "%Y-%m-%d")
    url = "http://localhost"
    location = "39.46,-0.36"

    processor = WeatherProcessor(url, "", "")
    processor.lookup = lambda _: location

    for xml_data, date in zip(ALL_DAYS_XML, [start_date - timedelta(days=n) for n in range(7)]):
        date_str = date.strftime("%Y-%m-%d")
        expected_response = Response(200, content=xml_data)
        respx.get(_build_url(url, location, date_str)).mock(return_value=expected_response)

    result = await processor.get("", start_date)
    assert result == expected_result
