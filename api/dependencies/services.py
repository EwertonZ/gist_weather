from config import OPENWEATHER_API_KEY, GITHUB_TOKEN
from services.weather_service import WeatherService
from services.gist_service import GistService

_weather_service = WeatherService(OPENWEATHER_API_KEY)
_gist_service = GistService(GITHUB_TOKEN)

def get_weather_service() -> WeatherService:
    return _weather_service


def get_gist_service() -> GistService:
    return _gist_service