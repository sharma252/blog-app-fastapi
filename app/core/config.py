import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")


class Settings:
    PROJECT_NAME = "Blog App - FastAPI"
    PROJECT_VERSION = "1.0.0"

    DATABASE_URL = os.getenv("DATABASE_URL")
    SECRET_KEY = os.getenv("SECRET_KEY")

    JWT_ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRES_MINUTES = 60 * 24


settings = Settings()
