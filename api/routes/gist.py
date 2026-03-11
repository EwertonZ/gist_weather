from pydantic import BaseModel, Field
from fastapi.routing import APIRouter
from services.weather_service import WeatherService
from config import OPENWEATHER_API_KEY

weather_service = WeatherService(OPENWEATHER_API_KEY)
router: APIRouter = APIRouter(prefix="/gist", tags=["gist"])

class GistCommentRequest(BaseModel):
    gist_id: str = Field(
        ..., 
        description="The ID of the GitHub Gist to comment on.",
        examples=["aa5a315d61ae9438b18d"]
    )
    city: str = Field(
        ...,
        description="The name of the city for which to retrieve weather information.",
        examples=["São Paulo"]
    )
    country_code: str | None = Field(
        None,
        description="The country code (ISO 3166-1 alpha-2) for more accurate location matching.",
        examples=["BR"]
    )
    state_code: str | None = Field(
        None,
        description="The state code (ISO 3166-2) for more accurate location matching.",
        examples=["SP"]
    )

@router.post("/comment")
async def comment_on_gist(request: GistCommentRequest):
    """
    Comment on a GitHub Gist with the current weather information for a specified location.
    """
    weather_summary = weather_service.get_weather_summary(
        city=request.city,
        country_code=request.country_code,
        state_code=request.state_code
    )

    return {"message": f"Commented on Gist {request.gist_id} with weather summary: {weather_summary}"}

