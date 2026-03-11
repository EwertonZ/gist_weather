from pydantic import BaseModel, Field


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