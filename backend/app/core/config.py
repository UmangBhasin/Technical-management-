import os
from datetime import timedelta

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'event_management.db')}"
SECRET_KEY = os.getenv("SECRET_KEY", "change-this-in-production-very-long-secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))
SESSION_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
CORS_ORIGINS = ["*"]

ADMIN_DEFAULT_EMAIL = "admin@events.com"
ADMIN_DEFAULT_PASSWORD = "Admin@123"
ADMIN_DEFAULT_NAME = "System Admin"


def access_token_expires_delta() -> timedelta:
    return timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
