from pydantic import BaseModel, Field
from fastapi import HTTPException
from fastapi.routing import APIRouter
from config import OPENWEATHER_API_KEY, GITHUB_TOKEN
from services.weather_service import WeatherService
from services.gist_service import GistService
from api.docs.gist_docs import (
    COMMENT_ON_GIST_SUMMARY,
    COMMENT_ON_GIST_DESCRIPTION,
    COMMENT_ON_GIST_RESPONSES,
)

weather_service = WeatherService(OPENWEATHER_API_KEY)
gist_service = GistService(GITHUB_TOKEN)
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

@router.post(
        "/comment",
        summary=COMMENT_ON_GIST_SUMMARY,
        description=COMMENT_ON_GIST_DESCRIPTION,
        responses=COMMENT_ON_GIST_RESPONSES # pyright: ignore[reportArgumentType]
)
async def comment_on_gist(request: GistCommentRequest):
    """
    Comment on a GitHub Gist with the current weather information for a specified location.
    """
    try:

        gist_service.validate_gist(request.gist_id)

        weather_summary = weather_service.get_weather_summary(
            city=request.city,
            country_code=request.country_code,
            state_code=request.state_code
        )

        gist_service.create_comment(gist_id=request.gist_id, comment=weather_summary)

        return {"message": f"Commented on Gist {request.gist_id} with weather summary: {weather_summary}"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except RuntimeError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Unexpected error while commenting on Gist"
        )
    

