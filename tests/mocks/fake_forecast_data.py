from openweather_sdk.models import ForecastData, WeatherData

def create_fake_forecast_data() -> list[ForecastData]:
    return [
        ForecastData(
            timestamp=1710000000,
            dt_txt="2026-03-11 00:00:00", 
            weather=WeatherData(
                temperature=20.0,
                feels_like=19.0,
                min_temperature=18.0,
                max_temperature=22.0,
                pressure=1010,
                humidity=50,
                description="clear sky",
                icon="01d"
            )
        ),
        ForecastData(
            timestamp=1710003600,
            dt_txt="2026-03-11 03:00:00", 
            weather=WeatherData(
                temperature=22.0,
                feels_like=21.0,
                min_temperature=20.0,
                max_temperature=24.0,
                pressure=1012,
                humidity=45,
                description="few clouds",
                icon="02d"
            )
        ),
        ForecastData(
            timestamp=1710000000,
            dt_txt="2026-03-12 00:00:00", 
            weather=WeatherData(
                temperature=20.0,
                feels_like=19.0,
                min_temperature=18.0,
                max_temperature=22.0,
                pressure=1010,
                humidity=50,
                description="clear sky",
                icon="01d"
            )
        ),
        ForecastData(
            timestamp=1710003600,
            dt_txt="2026-03-12 03:00:00", 
            weather=WeatherData(
                temperature=22.0,
                feels_like=21.0,
                min_temperature=20.0,
                max_temperature=24.0,
                pressure=1012,
                humidity=45,
                description="few clouds",
                icon="02d"
            )
        ),
        ForecastData(
            timestamp=1710086400,
            dt_txt="2026-03-13 00:00:00", 
            weather=WeatherData(
                temperature=18.0,
                feels_like=17.0,
                min_temperature=16.0,
                max_temperature=20.0,
                pressure=1008,
                humidity=55,
                description="scattered clouds",
                icon="03d"
            )
        ),
        ForecastData(
            timestamp=1710090000,
            dt_txt="2026-03-13 03:00:00", 
            weather=WeatherData(
                temperature=20.0,
                feels_like=19.0,
                min_temperature=18.0,
                max_temperature=22.0,
                pressure=1011,
                humidity=50,
                description="broken clouds",
                icon="04d"
            )
        ),
    ]