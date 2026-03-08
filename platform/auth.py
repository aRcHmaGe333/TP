import base64
import hashlib
import hmac
import secrets
from typing import Dict, Tuple
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
try:
    from . import config
except ImportError:  # pragma: no cover - local-module execution fallback
    import config
def hash_password(password: str, salt: bytes | None = None) -> Tuple[str, str]:
    salt = salt or secrets.token_bytes(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return base64.b64encode(salt).decode(), base64.b64encode(hashed).decode()
def verify_password(password: str, salt_b64: str, hash_b64: str) -> bool:
    salt = base64.b64decode(salt_b64.encode())
    expected = base64.b64decode(hash_b64.encode())
    candidate = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 120000)
    return hmac.compare_digest(candidate, expected)
def build_signing_key() -> str:
    return base64.b64encode(secrets.token_bytes(32)).decode()
def make_signature(payload: Dict, signing_key_b64: str) -> str:
    signing_key = base64.b64decode(signing_key_b64.encode())
    normalized = repr(sorted(payload.items())).encode()
    digest = hmac.new(signing_key, normalized, hashlib.sha256).digest()
    return base64.b64encode(digest).decode()
def fingerprint(signing_key_b64: str) -> str:
    raw = base64.b64decode(signing_key_b64.encode())
    digest = hashlib.sha256(raw).hexdigest()
    return "FPR-" + digest[:24]
def get_serializer(secret_key: str | None = None) -> URLSafeTimedSerializer:
    return URLSafeTimedSerializer(secret_key or config.get_secret(), salt="platform-session")
def create_token(user_id: int, secret_key: str | None = None) -> str:
    serializer = get_serializer(secret_key)
    return serializer.dumps({"uid": user_id})
def load_token(token: str, secret_key: str | None = None) -> int | None:
    try:
        serializer = get_serializer(secret_key)
        data = serializer.loads(token, max_age=config.get_session_max_age())
        return int(data.get("uid"))
    except (BadSignature, SignatureExpired, ValueError):
        return None
