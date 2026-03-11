import pytest
from github import GithubException
from mocks.fake_gist_client import FakeGist
from services.gist_service import GistService


def test_validate_gist(monkeypatch):

    service = GistService(token="fake")

    def fake_get_gist(gist_id):
        return FakeGist()

    monkeypatch.setattr(service.github, "get_gist", fake_get_gist)

    result = service.validate_gist("123")

    assert result is None

def test_validate_gist_error(monkeypatch):

    service = GistService(token="fake")

    def fake_get_gist(gist_id):
        raise RuntimeError("GitHub error")

    monkeypatch.setattr(service.github, "get_gist", fake_get_gist)

    with pytest.raises(RuntimeError):
        service.validate_gist("123")

def test_create_comment(monkeypatch):

    service = GistService(token="fake")

    fake_gist = FakeGist()

    def fake_get_gist(gist_id):
        return fake_gist

    monkeypatch.setattr(service.github, "get_gist", fake_get_gist)

    service.create_comment("123", "hello")

    assert fake_gist.comment == "hello"

def test_create_comment_empty_comment():

    service = GistService(token="fake")

    with pytest.raises(ValueError):
        service.create_comment("123", "")

@pytest.mark.parametrize(
    "status,expected_exception",
    [
        (404, ValueError),
        (401, PermissionError),
        (403, PermissionError),
        (500, RuntimeError),
    ],
)
def test_create_comment_github_errors(monkeypatch, status, expected_exception):

    service = GistService(token="fake")

    def fake_get_gist(gist_id):
        raise GithubException(status, {"message": "error"}, None)

    monkeypatch.setattr(service.github, "get_gist", fake_get_gist)

    with pytest.raises(expected_exception):
        service.create_comment("123", "hello")

@pytest.mark.parametrize(
    "status,expected_exception",
    [
        (404, ValueError),
        (401, PermissionError),
        (403, PermissionError),
        (500, RuntimeError),
    ],
)
def test_validate_gist_exceptions(monkeypatch, status, expected_exception):

    service = GistService(token="fake")

    def fake_get_gist(gist_id):
        raise GithubException(status, {"message": "error"}, None)

    monkeypatch.setattr(service.github, "get_gist", fake_get_gist)

    with pytest.raises(expected_exception):
        service.validate_gist("123")