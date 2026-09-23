from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "AI Attendance System API"
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    # Database — SQLite locally, Neon Postgres in production (free tier).
    # Example prod value: postgresql+psycopg://user:pass@host/dbname
    database_url: str = "sqlite:///./attendance.db"

    # Security
    jwt_secret_key: str = "dev-only-secret-key-change-me-in-production-32+bytes"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h for dev; tighten in prod
    refresh_token_expire_days: int = 14


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
