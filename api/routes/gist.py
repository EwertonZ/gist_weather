from pydantic import BaseModel
from fastapi.routing import APIRouter

router: APIRouter = APIRouter(prefix="/gist", tags=["gist"])

class GistCommentRequest(BaseModel):
    gist_id: str
    city: str
    country_code: str | None = None
    state_code: str | None = None

@router.post("/comment")
async def comment_on_gist(request: GistCommentRequest):
    """
    Comment on a GitHub Gist with the current weather information for a specified location.

    - **gist_id**: The ID of the GitHub Gist to comment on.
    - **city**: The name of the city for which to retrieve weather information.
    - **country_code**: (Optional) The country code (ISO 3166-1 alpha-2) for more accurate location matching.
    - **state_code**: (Optional) The state code (ISO 3166-2) for more accurate location matching.
    """
    # This function will be implemented in the main application file where the weather service and GitHub API integration are handled.
    pass

