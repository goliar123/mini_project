import json
import os

import firebase_admin
from firebase_admin import credentials, db

from app.config import FIREBASE_CREDENTIALS_PATH, FIREBASE_DB_URL, POTHOLES_PATH, USERS_PATH


def _load_firebase_credential() -> credentials.Base:
    raw_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
    if raw_json:
        return credentials.Certificate(json.loads(raw_json))

    try:
        import streamlit as st

        secret_block = st.secrets.get("firebase_service_account")
        if secret_block:
            return credentials.Certificate(dict(secret_block))
    except Exception:
        pass

    return credentials.Certificate(FIREBASE_CREDENTIALS_PATH)


def initialize_firebase() -> None:
    if firebase_admin._apps:
        return

    try:
        cred = _load_firebase_credential()
        firebase_admin.initialize_app(
            cred,
            {
                "databaseURL": FIREBASE_DB_URL,
            },
        )
    except Exception:
        # Keep behavior aligned with existing app: fail silently during init.
        pass


def potholes_ref():
    return db.reference(POTHOLES_PATH)


def users_ref():
    return db.reference(USERS_PATH)
