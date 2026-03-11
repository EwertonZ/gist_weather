COMMENT_ON_GIST_SUMMARY = "Comment on a GitHub Gist with weather information"

COMMENT_ON_GIST_DESCRIPTION = """
This endpoint retrieves the current weather information for a specified location
and posts it as a comment on a specified GitHub Gist.

The weather information is formatted in Markdown and includes an icon representing
the current weather conditions.
"""

COMMENT_ON_GIST_RESPONSES = {
    400: {"description": "Invalid request or bad data"},
    403: {"description": "Permission denied or GitHub API rate limit exceeded"},
    500: {"description": "Internal server error"},
}