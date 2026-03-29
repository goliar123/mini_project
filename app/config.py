import os

FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "serviceAccountKey.json")
FIREBASE_DB_URL = os.getenv(
    "FIREBASE_DB_URL", "https://pothole-detection-22105-default-rtdb.firebaseio.com/"
)
POTHOLES_PATH = "/potholes"
USERS_PATH = "/users"

DEFAULT_MAP_LAT = 17.5200
DEFAULT_MAP_LNG = 78.3600
COORD_ROUNDING = 4

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
MIN_PASSWORD_LENGTH = int(os.getenv("MIN_PASSWORD_LENGTH", "6"))
SESSION_TOKEN_SECRET = os.getenv("SESSION_TOKEN_SECRET", "change-this-session-token-secret")
SESSION_TOKEN_MAX_AGE_SECONDS = int(os.getenv("SESSION_TOKEN_MAX_AGE_SECONDS", "28800"))
