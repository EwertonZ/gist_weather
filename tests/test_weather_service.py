from services.weather_service import WeatherService
from openweather_sdk.models import WeatherData
from mocks.fake_forecast_data import create_fake_forecast_data


def test_group_and_get_daily_forecast_mean():

    service = WeatherService(api_key="fake")

    forecast = create_fake_forecast_data()

    result = service._group_and_get_daily_forecast_mean(forecast)

    assert result["2026-03-12"] == 21
    assert result["2026-03-13"] == 19


def test_generate_weather_summary():

    service = WeatherService(api_key="fake")

    weather = WeatherData(
        temperature=20,
        feels_like=19,
        min_temperature=18,
        max_temperature=22,
        pressure=1010,
        humidity=50,
        description="clear sky",
        icon="01d"
    )

    daily_means = {
        "2026-03-12": 21.00,
        "2026-03-13": 19.00,
    }

    result = service._generate_weather_summary(
        city="São Paulo",
        weather_data=weather,
        daily_means=daily_means
    )

    assert "São Paulo" in result
    assert "21°C" in result


def test_get_weather_summary(monkeypatch):

    service = WeatherService(api_key="fake")

    def fake_get_coordinates(city, country_code=None, state_code=None):
        return {"lat": -23.55, "lon": -46.63}

    def fake_get_current_weather(coords):
        return WeatherData(
            temperature=20,
            feels_like=19,
            min_temperature=18,
            max_temperature=22,
            pressure=1010,
            humidity=50,
            description="clear sky",
            icon="01d"
        )

    def fake_get_forecast(coords):
        return create_fake_forecast_data()

    monkeypatch.setattr(service.client, "get_coordinates", fake_get_coordinates)
    monkeypatch.setattr(service.client, "get_current_weather", fake_get_current_weather)
    monkeypatch.setattr(service.client, "get_forecast", fake_get_forecast)

    summary = service.get_weather_summary("São Paulo")

    assert "São Paulo" in summary


def test_get_weather_summary_city_not_found(monkeypatch):

    service = WeatherService(api_key="fake")

    def fake_get_coordinates(city, country_code=None, state_code=None):
        return None

    monkeypatch.setattr(service.client, "get_coordinates", fake_get_coordinates)

    result = service.get_weather_summary("CidadeFake")

    assert "Não foi possível encontrar informações climáticas" in result