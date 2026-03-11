from api.dependencies.services import (
    get_weather_service,
    get_gist_service,
)

from services.weather_service import WeatherService
from services.gist_service import GistService


def test_get_weather_service_returns_instance():

    service = get_weather_service()

    assert isinstance(service, WeatherService)


def test_get_gist_service_returns_instance():

    service = get_gist_service()

    assert isinstance(service, GistService)


def test_weather_service_is_singleton():

    service1 = get_weather_service()
    service2 = get_weather_service()

    assert service1 is service2


def test_gist_service_is_singleton():

    service1 = get_gist_service()
    service2 = get_gist_service()

    assert service1 is service2