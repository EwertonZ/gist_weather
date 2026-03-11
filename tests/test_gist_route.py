import pytest
from tests.mocks.fake_gist_service import FakeGistService


def test_comment_on_gist_success(client):

    payload = {
        "gist_id": "123",
        "city": "São Paulo",
        "country_code": "BR",
        "state_code": "SP",
    }

    response = client.post("/gist/comment", json=payload)

    assert response.status_code == 200
    assert "Weather summary for São Paulo" in response.json()["message"]


@pytest.mark.parametrize(
    ("exception", "expected_status", "expected_detail"),
    [
        pytest.param(ValueError("Invalid gist"), 400, "Invalid gist", id="value-error"),
        pytest.param(PermissionError("Forbidden"), 403, "Forbidden", id="permission-error"),
        pytest.param(RuntimeError("GitHub API error"), 500, "GitHub API error", id="runtime-error"),
    ],
)
def test_comment_on_gist_known_errors(
    client,
    monkeypatch,
    exception,
    expected_status,
    expected_detail,
):

    def fake_validate_gist(self, gist_id):
        raise exception

    monkeypatch.setattr(FakeGistService, "validate_gist", fake_validate_gist)

    payload = {
        "gist_id": "123",
        "city": "São Paulo",
    }

    response = client.post("/gist/comment", json=payload)

    assert response.status_code == expected_status
    assert response.json()["detail"] == expected_detail


def test_comment_on_gist_unexpected_error(client, monkeypatch):

    def fake_validate_gist(self, gist_id):
        raise Exception("Unexpected")

    monkeypatch.setattr(FakeGistService, "validate_gist", fake_validate_gist)

    payload = {
        "gist_id": "123",
        "city": "São Paulo",
    }

    response = client.post("/gist/comment", json=payload)

    assert response.status_code == 500
    assert response.json()["detail"] == "Unexpected error while commenting on Gist"