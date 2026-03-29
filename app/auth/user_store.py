import hashlib
import re

from app.config import ADMIN_USERNAME


def normalize_username(username: str) -> str:
    cleaned = username.strip().lower()
    if not re.fullmatch(r"[a-z0-9_]{3,32}", cleaned):
        return ""
    return cleaned


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def create_user(username: str, password: str) -> bool:
    normalized = normalize_username(username)
    if not normalized or normalized == ADMIN_USERNAME.lower():
        return False

    try:
        from app.data.firebase_client import users_ref

        existing = users_ref().child(normalized).get()
        if existing:
            return False

        users_ref().child(normalized).set(
            {
                "username": normalized,
                "password_hash": _hash_password(password),
                "preferences": {"map_view_mode": "heatmap"},
            }
        )
        return True
    except Exception:
        return False


def verify_user(username: str, password: str) -> bool:
    normalized = normalize_username(username)
    if not normalized:
        return False

    try:
        from app.data.firebase_client import users_ref

        user_record = users_ref().child(normalized).get()
        if not user_record:
            return False

        return user_record.get("password_hash") == _hash_password(password)
    except Exception:
        return False


def get_user_map_view_mode(username: str) -> str | None:
    normalized = normalize_username(username)
    if not normalized:
        return None

    try:
        from app.data.firebase_client import users_ref

        pref = users_ref().child(normalized).child("preferences").child("map_view_mode").get()
        if pref in {"heatmap", "scatter"}:
            return pref
        return None
    except Exception:
        return None


def set_user_map_view_mode(username: str, mode: str) -> bool:
    normalized = normalize_username(username)
    if not normalized or mode not in {"heatmap", "scatter"}:
        return False

    try:
        from app.data.firebase_client import users_ref

        users_ref().child(normalized).child("preferences").child("map_view_mode").set(mode)
        return True
    except Exception:
        return False
