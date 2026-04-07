from __future__ import annotations

import datetime as dt
from dataclasses import dataclass

from itsdangerous import BadSignature, SignatureExpired, URLSafeTimedSerializer

try:
    from . import config
except ImportError:  # pragma: no cover - local-module execution fallback
    import config


IDENTITY_SALT = "ttp-identity-verification"


@dataclass(frozen=True)
class IdentityClaims:
    provider: str
    subject_key: str
    legal_name: str
    country_code: str
    verified_at: dt.datetime


def _get_serializer(secret_key: str | None = None) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key or config.get_secret(), salt=IDENTITY_SALT)


def normalize_provider(provider: str) -> str:
    return provider.strip().lower()


def build_subject_key(subject_id: str, country_code: str = "SE") -> str:
    return f"{country_code.strip().upper() or 'SE'}:{subject_id.strip()}"


def create_verification_token(claims: IdentityClaims, secret_key: str | None = None) -> str:
    serializer = _get_serializer(secret_key)
    return serializer.dumps(
        {
            "provider": claims.provider,
            "subject_key": claims.subject_key,
            "legal_name": claims.legal_name,
            "country_code": claims.country_code,
            "verified_at": claims.verified_at.isoformat(),
        }
    )


def load_verification_token(token: str, secret_key: str | None = None) -> IdentityClaims | None:
    serializer = _get_serializer(secret_key)
    try:
        data = serializer.loads(token, max_age=config.get_identity_token_max_age())
    except (BadSignature, SignatureExpired, ValueError):
        return None

    try:
        verified_at = dt.datetime.fromisoformat(data["verified_at"])
    except (KeyError, TypeError, ValueError):
        return None

    return IdentityClaims(
        provider=normalize_provider(data.get("provider", "")),
        subject_key=str(data.get("subject_key", "")).strip(),
        legal_name=str(data.get("legal_name", "")).strip(),
        country_code=str(data.get("country_code", "")).strip().upper() or "SE",
        verified_at=verified_at,
    )


def build_dev_claims(
    *,
    provider: str,
    subject_id: str,
    legal_name: str,
    country_code: str = "SE",
) -> IdentityClaims:
    normalized_provider = normalize_provider(provider)
    return IdentityClaims(
        provider=normalized_provider,
        subject_key=build_subject_key(subject_id, country_code),
        legal_name=legal_name.strip(),
        country_code=country_code.strip().upper() or "SE",
        verified_at=dt.datetime.utcnow(),
    )
