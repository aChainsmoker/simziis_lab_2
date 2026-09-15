import os
from pathlib import Path

from dotenv import load_dotenv


PROJECT_ROOT = Path(__file__).resolve().parents[2]
load_dotenv(PROJECT_ROOT / ".env")

DATABASE_URL = os.getenv("DATABASE_URL")
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
CONFIDENTIAL_DATA_KEY = os.getenv("CONFIDENTIAL_DATA_KEY")
ACCESS_TOKEN_COOKIE = "lab2_access_token"
CORS_ORIGINS = ["http://127.0.0.1:8000", "http://localhost:8000"]
