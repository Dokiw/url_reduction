from unittest.mock import MagicMock

import pytest
from fastapi import HTTPException

from handlers.service import ServiceReductionUrl
from test.fixture_until import repo


def test_create_and_get_short_url(repo):
    url = "https://example.com"
    code = repo.create_short_url(url)
    assert code is not None

    fetched_url = repo.get_short_url(code)
    assert fetched_url == url


def test_get_short_url_not_found(repo):
    assert repo.get_short_url("nonexistent") is None


# mock - для обработки логики:

def test_get_short_url_success():
    mock_repo = MagicMock()
    mock_repo.get_short_url.return_value = "https://example.com"
    service = ServiceReductionUrl(mock_repo)

    url = service.get_short_url("abc123")
    assert url == "https://example.com"


def test_get_short_url_404():
    mock_repo = MagicMock()
    mock_repo.get_short_url.return_value = None
    service = ServiceReductionUrl(mock_repo)

    with pytest.raises(HTTPException) as exc:
        service.get_short_url("notfound")
    assert exc.value.status_code == 404


def start_testing():
    # unit - repo
    test_get_short_url_not_found(repo)
    test_create_and_get_short_url(repo)

    # service - test
    test_get_short_url_success()
    test_get_short_url_404()


if __name__ == "__main__":
    start_testing()
