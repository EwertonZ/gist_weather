from fastapi import HTTPException, Depends
from fastapi.routing import APIRouter
from services.weather_service import WeatherService
from services.gist_service import GistService
from schemas.gist import GistCommentRequest
from api.dependencies.services import (
    get_weather_service,
    get_gist_service,
)
from api.docs.gist_docs import (
    COMMENT_ON_GIST_SUMMARY,
    COMMENT_ON_GIST_DESCRIPTION,
    COMMENT_ON_GIST_RESPONSES,
)


router: APIRouter = APIRouter(prefix="/gist", tags=["gist"])

@router.post(
        "/comment",
        summary=COMMENT_ON_GIST_SUMMARY,
        description=COMMENT_ON_GIST_DESCRIPTION,
        responses=COMMENT_ON_GIST_RESPONSES # pyright: ignore[reportArgumentType]
)
async def comment_on_gist(
    request: GistCommentRequest,
    weather_service: WeatherService = Depends(get_weather_service),
    gist_service: GistService = Depends(get_gist_service),
):
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
    

