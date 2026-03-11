from github.Gist import Gist
from github import Github, Auth
from github.GithubException import GithubException
from core.logging import get_logger


logger = get_logger(__name__)

class GistService:

    def __init__(self, token: str):
        self.auth = Auth.Token(token)
        self.github = Github(auth=self.auth)
    
    def validate_gist(self, gist_id: str) -> None:
        """
        Validates the existence of a GitHub Gist.

        Args:
            gist_id: The ID of the GitHub Gist to validate.
        
        Raises:
            ValueError: If the Gist is not found.
            PermissionError: If the GitHub token is invalid or lacks permissions.
            RuntimeError: For other GitHub API errors.
        """
        logger.info("Validating Gist with ID=%s", gist_id)
        try:
            self.github.get_gist(gist_id)
        except GithubException as e:
            logger.error("Error validating Gist with ID=%s: %s", gist_id, e)
            if e.status == 404:
                raise ValueError("Gist not found")

            if e.status == 401:
                raise PermissionError("Invalid GitHub token")

            if e.status == 403:
                raise PermissionError("Permission denied or rate limit exceeded")

            raise RuntimeError("GitHub API error")

    def create_comment(self, gist_id: str, comment: str):
        """
        Creates a comment on a GitHub Gist.

        Args:
            gist_id: The ID of the GitHub Gist to comment on.
            comment: The content of the comment to post.
        
        Raises:
            ValueError: If the comment is empty or the Gist is not found.
            PermissionError: If the GitHub token is invalid or lacks permissions.
            RuntimeError: For other GitHub API errors.
        """

        if not comment.strip():
            raise ValueError("Comment cannot be empty")

        logger.info("Creating comment on Gist with ID=%s", gist_id)
        try:
            gist: Gist = self.github.get_gist(gist_id)
            gist.create_comment(comment)
            logger.info("Comment created on Gist with ID=%s", gist_id)
        except GithubException as e:
            logger.error("Error creating comment on Gist with ID=%s: %s", gist_id, e)
            if e.status == 404:
                raise ValueError(f"Gist '{gist_id}' not found")

            if e.status == 401:
                raise PermissionError("Invalid GitHub token")

            if e.status == 403:
                raise PermissionError("GitHub API rate limit exceeded")

            raise RuntimeError(f"GitHub API error: {e.data}")