import pytest
from fastapi.testclient import TestClient
from main import app

from api.dependencies.services import (
    get_weather_service,
    get_gist_service,
)

from tests.mocks.fake_weather_service import FakeWeatherService
from tests.mocks.fake_gist_service import FakeGistService


@pytest.fixture
def client():

    app.dependency_overrides[get_weather_service] = lambda: FakeWeatherService()
    app.dependency_overrides[get_gist_service] = lambda: FakeGistService()

    client = TestClient(app)

    yield client

    app.dependency_overrides.clear()