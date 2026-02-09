import pytest

from handlers.repo import Repository_short_url


@pytest.fixture
def repo():
    #фикстура для симуляции соединения бд в памяти

    from engine import get_db, DB_FILE
    DB_FILE = ":memory:"
    repo = Repository_short_url()
    repo.refill_pool(10)
    return repo