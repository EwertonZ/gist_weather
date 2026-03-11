class FakeWeatherService:
    
    def get_weather_summary(self, city, country_code=None, state_code=None):
        return f"Weather summary for {city}"