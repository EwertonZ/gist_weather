import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPEN_WEATHER_API_KEY", "your_default_api_key_here")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "your_default_github_token_here")