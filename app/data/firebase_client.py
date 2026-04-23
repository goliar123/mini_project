import logging

import firebase_admin
from firebase_admin import credentials, db

from app.config import FIREBASE_CREDENTIALS_PATH, FIREBASE_DB_URL, POTHOLES_PATH, USERS_PATH


logger = logging.getLogger(__name__)


def _load_firebase_credential() -> credentials.Base:
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
    except Exception as exc:
        # Surface startup issues in logs so Firebase connection problems are diagnosable.
        logger.exception("Firebase initialization failed: %s", exc)


def potholes_ref():
    return db.reference(POTHOLES_PATH)


def users_ref():
    return db.reference(USERS_PATH)
