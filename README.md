### Gist Weather API

A simple weather API built with FastAPI to comment on GitHub Gists with weather information.

### Features

- Validate GitHub Gists existence
- Fetch current weather and 5-day forecast for cities
- Automatically post weather comments on Gists based on city mentions

### Prerequisites

- Python 3.11 or higher
- GitHub Personal Access Token with gist permissions
- OpenWeather API Key

### Installation

1. Clone the repository:
```bash
git clone https://github.com/EwertonZ/gist_weather.git
cd gist_weather
```

2. Install dependencies with UV
```bash
uv sync
```

3. Activate .venv enviroment
```bash
source .venv/bin/activate
```

4. Create a .env file in the root dicretory with yout API keys:
```
GITHUB_TOKEN=your_github_personal_access_token
OPENWEATHER_API_KEY=your_openweather_api_key
```

### Usage

Running Locally

Start the FastAPI server:
```bash
fastapi run
```
The API will be available at http://localhost:8000
#### API Documentation
Visit http://localhost:8000/docs for interactive API documentation.

### API Endpoints
##### POST /gist/{gist_id}/comment
Creates a weather comment on the specified GitHub Gist.

###### Request Body:
```JSON
{
  "gist_id": "your_gist_id",  
  "city": "São Paulo",
  "country_code": "BR",
  "state_code": "SP"
}
```
##### Response:
- `200 OK`: Comment successfully created
- `400 Bad Request`: Invalid request or city not found
- `404 Not Found`: Gist not found
- `401 Unauthorized`: Invalid GitHub token
- `403 Forbidden`: Insufficient permissions

##### Example Response:
```
Comment created successfully.
```

### Development

##### Installing Development Dependencies
```bash
uv sync --extra dev
```

###### Running Tests
```bash
pytest
```

### Docker
```bash
docker compose up --build
```

### License
This project is licensed under the MIT License - see the LICENSE file for details.

### Acknowledgments
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [PyGitHub](https://pygithub.readthedocs.io/) - GitHub API library
- [OpenWeather SDK](https://github.com/EwertonZ/open-weather-sdk) - Weather API SDK


