import firebase_admin
from firebase_admin import credentials, db

from app.config import FIREBASE_CREDENTIALS_PATH, FIREBASE_DB_URL, POTHOLES_PATH, USERS_PATH


def initialize_firebase() -> None:
    if firebase_admin._apps:
        return

    try:
        cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
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
