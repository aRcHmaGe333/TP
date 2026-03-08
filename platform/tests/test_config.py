import pathlib
import sys
import pytest
ROOT = pathlib.Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
PROJECT_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
import config
def test_validate_runtime_config_requires_non_default_secret(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PLATFORM_ENV", "prod")
    monkeypatch.delenv("PLATFORM_DATABASE_URL", raising=False)
    monkeypatch.delenv("PLATFORM_CORS_ORIGINS", raising=False)
    monkeypatch.delenv("PLATFORM_SECRET", raising=False)
    with pytest.raises(RuntimeError):
        config.validate_runtime_config()
def test_validate_runtime_config_rejects_wildcard_cors(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("PLATFORM_SECRET", "non-default")
    monkeypatch.setenv("PLATFORM_DATABASE_URL", "postgresql+psycopg://u:p@localhost/db")
    monkeypatch.setenv("PLATFORM_CORS_ORIGINS", "*")
