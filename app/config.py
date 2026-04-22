import os


def _read_setting(name: str, default: str) -> str:
    env_value = os.getenv(name)
    if env_value:
        return env_value

    try:
        import streamlit as st

        secret_value = st.secrets.get(name)
        if secret_value:
            return str(secret_value)
    except Exception:
        pass

    return default


def _read_int_setting(name: str, default: int) -> int:
    raw_value = _read_setting(name, str(default))
    try:
        return int(raw_value)
    except (TypeError, ValueError):
        return default

FIREBASE_CREDENTIALS_PATH = _read_setting("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
FIREBASE_DB_URL = _read_setting(
    "FIREBASE_DB_URL", "https://pothhole-detect-default-rtdb.firebaseio.com/"
)
POTHOLES_PATH = "/potholes"
USERS_PATH = "/users"

DEFAULT_MAP_LAT = 17.5200
DEFAULT_MAP_LNG = 78.3600
COORD_ROUNDING = 4

ADMIN_USERNAME = _read_setting("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = _read_setting("ADMIN_PASSWORD", "admin")
MIN_PASSWORD_LENGTH = _read_int_setting("MIN_PASSWORD_LENGTH", 6)
SESSION_TOKEN_SECRET = _read_setting("SESSION_TOKEN_SECRET", "change-this-session-token-secret")
SESSION_TOKEN_MAX_AGE_SECONDS = _read_int_setting("SESSION_TOKEN_MAX_AGE_SECONDS", 28800)
