from datetime import datetime
from statistics import mean
from openweather_sdk import (
    OpenWeatherClient,
    ForecastData,
    WeatherData,
)
from config import OPENWEATHER_API_KEY

class WeatherService:
    """
    Service class responsible for interacting with the OpenWeather API to retrieve current weather information, forecasts
    and generate weather summaries for specified locations.
    """
    def __init__(self, api_key: str = OPENWEATHER_API_KEY):
        self.client = OpenWeatherClient(api_key)
    
    def _group_and_get_daily_forecast_mean(
        self, forecast_data: list[ForecastData]
    ) -> dict[str, float]:
        """
        Group forecast data by date and calculate the mean temperature for each day.

        Args:
            forecast_data: A list of ForecastData objects containing the forecast information.
        
        Returns:
            A dictionary mapping date strings (YYYY-MM-DD) to mean temperatures for that date.
        
        Example:
            forecast_data = [
                ForecastData(dt_txt="2024-06-01 12:00:00", weather=WeatherData(temperature=20.0, ...)),
                ForecastData(dt_txt="2024-06-01 15:00:00", weather=WeatherData(temperature=22.0, ...)),
                ForecastData(dt_txt="2024-06-02 12:00:00", weather=WeatherData(temperature=18.0, ...)),
            ]
            daily_means = weather_service._group_and_get_daily_forecast_mean(forecast_data)
            print(daily_means)  # Output: {"2024-06-01": 21.0, "2024-06-02": 18.0}
        """ 

        today = datetime.now().date()

        daily_temps: dict[str, list[float]] = {}

        for forecast in forecast_data:
            date_str = forecast.dt_txt.split(" ")[0]
            date_obj = datetime.strptime(date_str, "%Y-%m-%d").date()

            if date_obj <= today:
                continue

            temp = forecast.weather.temperature

            if date_str not in daily_temps:
                daily_temps[date_str] = []

            daily_temps[date_str].append(temp)

        daily_means = {date: mean(temps) for date, temps in daily_temps.items()}

        # limit to the next 5 days
        daily_means = dict(list(daily_means.items())[:5])

        return daily_means
    
    def _generate_weather_summary(
        self, city: str, weather_data: WeatherData, daily_means: dict[str, float]
    ) -> str:
        """
        Generate a weather summary string based on current weather data and daily mean temperatures.

        Args:
            city: The name of the city for which to generate the summary.
            weather_data: A WeatherData object containing the current weather information.
            daily_means: A dictionary mapping date strings (YYYY-MM-DD) to mean temperatures for
                            the forecasted days.
        
        Returns:
            A Markdown formatted string summarizing the current weather conditions and the forecast for the upcoming days.

        Example:
            weather_data = WeatherData(temperature=25.0, description="Clear sky", ...)
            daily_means = {"2024-06-01": 21.0, "2024-06-02": 18.0}
            summary = weather_service._generate_weather_summary(weather_data, daily_means)
            print(summary)  # Output: "Current weather: Clear sky, 25°C. Forecast: 01/06: 21°C, 02/06: 18°C"
        """

        current_temp = round(weather_data.temperature)

        forecast_parts = []

        for date, temp in daily_means.items():

            date_obj = datetime.strptime(date, "%Y-%m-%d")
            formatted_date = date_obj.strftime("%d/%m")

            forecast_parts.append(f"{formatted_date}: {round(temp)}°C")

        forecast_summary = ", ".join(forecast_parts)

        markdown_summary =f"""
![Weather Icon](https://openweathermap.org/img/wn/{weather_data.icon}.png) 

### Temperatura atual para {datetime.now().strftime('%d/%m')}

{current_temp}°C e {weather_data.description.lower()} em {city}.

### Previsão para os próximos dias

{forecast_summary}.
"""
        
        return markdown_summary

    def get_weather_summary(self, city: str, country_code: str | None = None, state_code: str | None = None) -> str:
        """
        Retrieve the current weather summary for a specified location.
        
        Args:
            city: The name of the city to retrieve weather information for.
            country_code: Optional ISO 3166 country code to disambiguate cities with the same name.
            state_code: Optional state code to further disambiguate cities with the same name.
        
        Returns:
            A formatted string summarizing the current weather conditions for the specified location.
        
        Raises:
            AuthenticationError: If the API key is invalid or missing.
            RateLimitError: If the API rate limit has been exceeded.
            OpenWeatherError: For any other errors returned by the OpenWeather API.
        
        Example:
            weather_service = WeatherService()
            summary = weather_service.get_weather_summary(city="São Paulo", country_code="BR", state_code="SP")
            print(summary)  # Output: "Current weather in São Paulo, SP, BR: Clear sky, 25°C..."
        """

        coordinates = self.client.get_coordinates(city, country_code, state_code)
        if not coordinates:
            return f"Não foi possível encontrar informações climáticas para {city}."
        weather_data = self.client.get_current_weather(coordinates)
        forecast = self.client.get_forecast(coordinates)
        daily_means = self._group_and_get_daily_forecast_mean(forecast)
        summary = self._generate_weather_summary(city, weather_data, daily_means)
        return summary
        