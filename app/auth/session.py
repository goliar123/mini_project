import base64
import hashlib
import hmac
import json
import time

import streamlit as st

from app.auth.user_store import (
    create_user,
    get_user_map_view_mode,
    normalize_username,
    verify_user,
)
from app.config import ADMIN_PASSWORD, ADMIN_USERNAME, MIN_PASSWORD_LENGTH, SESSION_TOKEN_MAX_AGE_SECONDS, SESSION_TOKEN_SECRET


def _b64url_encode(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).decode("ascii").rstrip("=")


def _b64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode(data + padding)


def _sign(payload: str) -> str:
    digest = hmac.new(
        SESSION_TOKEN_SECRET.encode("utf-8"),
        payload.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    return _b64url_encode(digest)


def _create_auth_token(username: str, role: str) -> str:
    payload_obj = {
        "u": username,
        "r": role,
        "iat": int(time.time()),
    }
    payload = _b64url_encode(json.dumps(payload_obj, separators=(",", ":")).encode("utf-8"))
    signature = _sign(payload)
    return f"{payload}.{signature}"


def _verify_auth_token(token: str) -> dict | None:
    if not token or "." not in token:
        return None

    payload, signature = token.split(".", 1)
    expected = _sign(payload)
    if not hmac.compare_digest(signature, expected):
        return None

    try:
        payload_obj = json.loads(_b64url_decode(payload).decode("utf-8"))
    except Exception:
        return None

    issued_at = int(payload_obj.get("iat", 0))
    if issued_at <= 0 or int(time.time()) - issued_at > SESSION_TOKEN_MAX_AGE_SECONDS:
        return None

    username = str(payload_obj.get("u", "")).strip()
    role = str(payload_obj.get("r", "")).strip()
    if not username or role not in {"admin", "user"}:
        return None

    return payload_obj


def persist_auth_token(state: dict) -> None:
    if not state.get("logged_in") or not state.get("current_user") or not state.get("current_role"):
        return
    token = _create_auth_token(state["current_user"], state["current_role"])
    st.query_params["auth"] = token


def restore_auth_from_query_params(state: dict) -> bool:
    token = st.query_params.get("auth")
    parsed = _verify_auth_token(token)
    if not parsed:
        return False

    username = parsed["u"]
    role = parsed["r"]
    if role == "admin" and username.lower() == ADMIN_USERNAME.lower():
        state["logged_in"] = True
        state["current_user"] = ADMIN_USERNAME
        state["current_role"] = "admin"
        state["map_view_mode"] = "scatter"
        state["last_map_view_mode"] = "scatter"
        return True

    normalized = normalize_username(username)
    if not normalized:
        return False

    preferred_mode = get_user_map_view_mode(normalized) or "heatmap"
    state["logged_in"] = True
    state["current_user"] = normalized
    state["current_role"] = "user"
    state["map_view_mode"] = preferred_mode
    state["last_map_view_mode"] = preferred_mode
    return True


def clear_persisted_auth() -> None:
    if "auth" in st.query_params:
        del st.query_params["auth"]


def validate_credentials(username: str, password: str) -> bool:
    return username.strip().lower() == ADMIN_USERNAME.lower() and password == ADMIN_PASSWORD


def login(state: dict, username: str, password: str) -> tuple[bool, str]:
    if validate_credentials(username, password):
        state["logged_in"] = True
        state["current_user"] = ADMIN_USERNAME
        state["current_role"] = "admin"
        state["map_view_mode"] = "scatter"
        state["last_map_view_mode"] = "scatter"
        persist_auth_token(state)
        return True, "Welcome back, admin"

    normalized = normalize_username(username)
    if verify_user(normalized, password):
        preferred_mode = get_user_map_view_mode(normalized) or "heatmap"
        state["logged_in"] = True
        state["current_user"] = normalized
        state["current_role"] = "user"
        state["map_view_mode"] = preferred_mode
        state["last_map_view_mode"] = preferred_mode
        persist_auth_token(state)
        return True, "Login successful"

    return False, "Invalid credentials"


def register_user(username: str, password: str, confirm_password: str) -> tuple[bool, str]:
    normalized = normalize_username(username)
    if not normalized:
        return False, "Use 3-32 chars: lowercase letters, numbers, underscore"

    if normalized == ADMIN_USERNAME.lower():
        return False, "Admin cannot be registered"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"

    if password != confirm_password:
        return False, "Passwords do not match"

    if not create_user(normalized, password):
        return False, "Username already exists or registration service unavailable"

    return True, "Registration successful. Please login"


def logout(state: dict) -> None:
    clear_persisted_auth()
    state["logged_in"] = False
    state["current_user"] = None
    state["current_role"] = None
    state["show_auth_panel"] = False
    state["map_view_mode"] = "heatmap"
    state["last_map_view_mode"] = "heatmap"
