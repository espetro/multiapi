from freezegun import freeze_time
from httpx import AsyncClient
import pytest_asyncio
import pytest

from app import app
from model import SexType, RaceType


@pytest_asyncio.fixture
async def app_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_health(app_client):
    response = await app_client.get("/health")
    assert response.text == '"OK"'


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_life_expectancy(app_client):
    response = await app_client.get(f"life_expectancy/{SexType.female}/{RaceType.white}/1998")
    assert response.json() == {"average_life_expectancy": 83}


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_unemployment_rate(app_client):
    response = await app_client.get("unemployment/ny")
    assert response.json() == {"rate": 4.6}


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_trends_interest(app_client):
    query_parameters = {"phrase": "easter-egg", "start_date": "2022-04-08", "end_date": "2022-04-16"}

    response = await app_client.get("trends", params=query_parameters)
    assert response.json() == {'interest': [0, 0, 0, 0, 0, 0, 100, 0, 0]}


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_trends_interest_fails_with_wrong_date_format(app_client):
    query_parameters = {"phrase": "easter-egg", "start_date": "2022 04 08", "end_date": "2022-04-16"}

    response = await app_client.get("trends", params=query_parameters)
    assert response.status_code == 422  # Unprocessable Entity
    assert response.json() == {
        'detail': [{'loc': ['query', 'start_date'],
                    'msg': 'invalid date format',
                    'type': 'value_error.date'}]
    }


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_trends_interest_fails_without_phrase(app_client):
    response = await app_client.get("trends")
    assert response.status_code == 422  # Unprocessable Entity


@freeze_time("2022-04-18")
@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_weather_and_trends_interest_for_last_7_days(app_client):
    query_parameters = {"phrase": "easter-egg"}
    expected_response = [
        {'date': '2022-04-18',
         'interest': 0,
         'weather': {'UV index': 0,
                     'average temperature': '18.3 °C',
                     'forecast': 'Cloudy',
                     'humidity': '66.0%',
                     'max. temperature': '21.8 °C',
                     'max. wind speed': '15.8 km/h',
                     'min. temperature': '13.1 °C',
                     'rainfall': '0.0 mm',
                     'sunrise': '07:21 AM',
                     'sunset': '08:42 PM'}},
        {'date': '2022-04-17',
         'interest': 0,
         'weather': {'UV index': 0,
                     'average temperature': '19.9 °C',
                     'forecast': 'Sunny',
                     'humidity': '57.0%',
                     'max. temperature': '23.1 °C',
                     'max. wind speed': '17.3 km/h',
                     'min. temperature': '14.7 °C',
                     'rainfall': '0.0 mm',
                     'sunrise': '07:22 AM',
                     'sunset': '08:41 PM'}},
        {'date': '2022-04-16',
         'interest': 0,
         'weather': {'UV index': 0,
                     'average temperature': '21.6 °C',
                     'forecast': 'Sunny',
                     'humidity': '51.0%',
                     'max. temperature': '26.3 °C',
                     'max. wind speed': '25.6 km/h',
                     'min. temperature': '14.8 °C',
                     'rainfall': '0.0 mm',
                     'sunrise': '07:23 AM',
                     'sunset': '08:40 PM'}},
        {'date': '2022-04-15',
         'interest': 100,
         'weather': {'UV index': 0,
                     'average temperature': '19.4 °C',
                     'forecast': 'Partly cloudy',
                     'humidity': '56.0%',
                     'max. temperature': '23.1 °C',
                     'max. wind speed': '19.4 km/h',
                     'min. temperature': '12.8 °C',
                     'rainfall': '0.0 mm',
                     'sunrise': '07:25 AM',
                     'sunset': '08:39 PM'}},
        {'date': '2022-04-14',
         'interest': 0,
         'weather': {'UV index': 0,
                     'average temperature': '17.3 °C',
                     'forecast': 'Partly cloudy',
                     'humidity': '60.0%',
                     'max. temperature': '20.5 °C',
                     'max. wind speed': '34.2 km/h',
                     'min. temperature': '12.1 °C',
                     'rainfall': '1.2 mm',
                     'sunrise': '07:26 AM',
                     'sunset': '08:38 PM'}},
        {'date': '2022-04-13',
         'interest': 0,
         'weather': {'UV index': 0,
                     'average temperature': '14.4 °C',
                     'forecast': 'Light rain shower',
                     'humidity': '86.0%',
                     'max. temperature': '18.0 °C',
                     'max. wind speed': '18.4 km/h',
                     'min. temperature': '12.6 °C',
                     'rainfall': '4.6 mm',
                     'sunrise': '07:28 AM',
                     'sunset': '08:37 PM'}}
    ]

    response = await app_client.get("trends_weather", params=query_parameters)
    assert response.json() == expected_response


@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_weather_and_trends_fails_without_phrase(app_client):
    response = await app_client.get("trends_weather")
    assert response.status_code == 422


@freeze_time("2022-04-18")
@pytest.mark.asyncio
@pytest.mark.integration_test
async def test_weather_for_last_7_days(app_client):
    expected_response = [
        {'UV index': 0,
         'average temperature': '18.3 °C',
         'date': '2022-04-18',
         'forecast': 'Cloudy',
         'humidity': '66.0%',
         'max. temperature': '21.8 °C',
         'max. wind speed': '15.8 km/h',
         'min. temperature': '13.1 °C',
         'rainfall': '0.0 mm',
         'sunrise': '07:21 AM',
         'sunset': '08:42 PM'},
        {'UV index': 0,
         'average temperature': '19.9 °C',
         'date': '2022-04-17',
         'forecast': 'Sunny',
         'humidity': '57.0%',
         'max. temperature': '23.1 °C',
         'max. wind speed': '17.3 km/h',
         'min. temperature': '14.7 °C',
         'rainfall': '0.0 mm',
         'sunrise': '07:22 AM',
         'sunset': '08:41 PM'},
        {'UV index': 0,
         'average temperature': '21.6 °C',
         'date': '2022-04-16',
         'forecast': 'Sunny',
         'humidity': '51.0%',
         'max. temperature': '26.3 °C',
         'max. wind speed': '25.6 km/h',
         'min. temperature': '14.8 °C',
         'rainfall': '0.0 mm',
         'sunrise': '07:23 AM',
         'sunset': '08:40 PM'},
        {'UV index': 0,
         'average temperature': '19.4 °C',
         'date': '2022-04-15',
         'forecast': 'Partly cloudy',
         'humidity': '56.0%',
         'max. temperature': '23.1 °C',
         'max. wind speed': '19.4 km/h',
         'min. temperature': '12.8 °C',
         'rainfall': '0.0 mm',
         'sunrise': '07:25 AM',
         'sunset': '08:39 PM'},
        {'UV index': 0,
         'average temperature': '17.3 °C',
         'date': '2022-04-14',
         'forecast': 'Partly cloudy',
         'humidity': '60.0%',
         'max. temperature': '20.5 °C',
         'max. wind speed': '34.2 km/h',
         'min. temperature': '12.1 °C',
         'rainfall': '1.2 mm',
         'sunrise': '07:26 AM',
         'sunset': '08:38 PM'},
        {'UV index': 0,
         'average temperature': '14.4 °C',
         'date': '2022-04-13',
         'forecast': 'Light rain shower',
         'humidity': '86.0%',
         'max. temperature': '18.0 °C',
         'max. wind speed': '18.4 km/h',
         'min. temperature': '12.6 °C',
         'rainfall': '4.6 mm',
         'sunrise': '07:28 AM',
         'sunset': '08:37 PM'},
        {'UV index': 0,
         'average temperature': '14.8 °C',
         'date': '2022-04-12',
         'forecast': 'Light rain shower',
         'humidity': '80.0%',
         'max. temperature': '17.7 °C',
         'max. wind speed': '11.2 km/h',
         'min. temperature': '11.7 °C',
         'rainfall': '0.7 mm',
         'sunrise': '07:29 AM',
         'sunset': '08:36 PM'}
    ]

    response = await app_client.get("weather")
    assert response.json() == expected_response


if __name__ == '__main__':
    pytest.main()
