from __future__ import annotations

import pathlib
import sys

import pytest
from fastapi.testclient import TestClient

ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _sqlite_url(path: pathlib.Path) -> str:
    return f"sqlite:///{path.as_posix()}"


@pytest.fixture
def client(tmp_path: pathlib.Path, monkeypatch: pytest.MonkeyPatch) -> TestClient:
    db_path = tmp_path / "test_platform.db"
    monkeypatch.setenv("PLATFORM_ENV", "dev")
    monkeypatch.setenv("PLATFORM_DATABASE_URL", _sqlite_url(db_path))
    monkeypatch.setenv("PLATFORM_SECRET", "test-secret")
    monkeypatch.setenv("PLATFORM_ADMIN_DISPLAY_NAMES", "admin")
    monkeypatch.setenv("PLATFORM_MAX_PAGE_SIZE", "2")
    monkeypatch.setenv("PLATFORM_DEFAULT_PAGE_SIZE", "2")
    monkeypatch.setenv("PLATFORM_MAX_REQUEST_BYTES", "2048")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_WINDOW_SECONDS", "60")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_REGISTER_PER_IP", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_LOGIN_PER_IP", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_IDEA_PER_IP", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_IDEA_PER_USER", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_VOTE_PER_IP", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_VOTE_PER_USER", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_COMMENT_PER_IP", "100")
    monkeypatch.setenv("PLATFORM_RATE_LIMIT_COMMENT_PER_USER", "100")

    project_root = pathlib.Path(__file__).resolve().parents[1]
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))

    import database

    database.get_cached_engine.cache_clear()
    database.init_db()

    from main import app

    with TestClient(app) as test_client:
        yield test_client
