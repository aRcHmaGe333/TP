import os
from dataclasses import dataclass
from typing import Set
DEFAULT_SECRET = "dev-secret-change-me"
def _get_int(name: str, default: int, minimum: int = 1) -> int:
    raw = os.getenv(name)
    if raw is None:
        return default
    try:
        value = int(raw)
    except ValueError as exc:
        raise RuntimeError(f"{name} must be an integer") from exc
    if value < minimum:
        raise RuntimeError(f"{name} must be >= {minimum}")
    return value
@dataclass(frozen=True)
class RateLimitConfig:
    window_seconds: int
    register_per_ip: int
    login_per_ip: int
    idea_per_ip: int
    idea_per_user: int
    vote_per_ip: int
    vote_per_user: int
    comment_per_ip: int
    comment_per_user: int
def get_env() -> str:
    return os.getenv("PLATFORM_ENV", "dev").strip().lower()
def is_dev_env() -> bool:
    return get_env() == "dev"
def get_secret() -> str:
    return os.getenv("PLATFORM_SECRET", DEFAULT_SECRET)
def get_session_max_age() -> int:
    return _get_int("PLATFORM_SESSION_MAX_AGE", 604800)
def get_database_url() -> str:
    value = os.getenv("PLATFORM_DATABASE_URL")
    if value:
        return value
    if is_dev_env():
        return "sqlite:///./platform.db"
    return ""
def get_cors_origins() -> list[str]:
    raw = os.getenv("PLATFORM_CORS_ORIGINS")
    if raw is None or raw.strip() == "":
        return ["*"] if is_dev_env() else []
    origins = [origin.strip() for origin in raw.split(",") if origin.strip()]
    return origins
def get_admin_display_names() -> Set[str]:
    raw = os.getenv("PLATFORM_ADMIN_DISPLAY_NAMES", "")
    return {name.strip().lower() for name in raw.split(",") if name.strip()}
def get_max_page_size() -> int:
    return _get_int("PLATFORM_MAX_PAGE_SIZE", 50)
def get_default_page_size() -> int:
    return _get_int("PLATFORM_DEFAULT_PAGE_SIZE", 20)
def get_max_request_bytes() -> int:
    return _get_int("PLATFORM_MAX_REQUEST_BYTES", 262144)
def get_rate_limits() -> RateLimitConfig:
    return RateLimitConfig(
        window_seconds=_get_int("PLATFORM_RATE_LIMIT_WINDOW_SECONDS", 60),
        register_per_ip=_get_int("PLATFORM_RATE_LIMIT_REGISTER_PER_IP", 20),
        login_per_ip=_get_int("PLATFORM_RATE_LIMIT_LOGIN_PER_IP", 60),
        idea_per_ip=_get_int("PLATFORM_RATE_LIMIT_IDEA_PER_IP", 30),
        idea_per_user=_get_int("PLATFORM_RATE_LIMIT_IDEA_PER_USER", 20),
        vote_per_ip=_get_int("PLATFORM_RATE_LIMIT_VOTE_PER_IP", 120),
        vote_per_user=_get_int("PLATFORM_RATE_LIMIT_VOTE_PER_USER", 60),
        comment_per_ip=_get_int("PLATFORM_RATE_LIMIT_COMMENT_PER_IP", 60),
        comment_per_user=_get_int("PLATFORM_RATE_LIMIT_COMMENT_PER_USER", 40),
    )
def validate_runtime_config() -> None:
    if is_dev_env():
        return
    secret = get_secret()
    if secret == DEFAULT_SECRET:
        raise RuntimeError("PLATFORM_SECRET must be set in non-dev environments")
    database_url = get_database_url()
    if not database_url:
        raise RuntimeError("PLATFORM_DATABASE_URL must be set in non-dev environments")
    origins = get_cors_origins()
    if not origins or "*" in origins:
        raise RuntimeError(
            "PLATFORM_CORS_ORIGINS must be a comma-separated allowlist in non-dev environments"
        )
