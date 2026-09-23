from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment / .env file."""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # App
    app_name: str = "AI Attendance System API"
    environment: str = "development"
    # Comma-separated list, e.g. "https://ai-attendance.vercel.app,http://localhost:3000"
    cors_origins: str = ""

    # Database — SQLite locally, Neon Postgres in production (free tier).
    # Example prod value: postgresql+psycopg://user:pass@host/dbname
    database_url: str = "sqlite:///./attendance.db"

    # Security
    jwt_secret_key: str = "dev-only-secret-key-change-me-in-production-32+bytes"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24  # 24h for dev; tighten in prod
    refresh_token_expire_days: int = 14

    @property
    def cors_origin_list(self) -> list[str]:
        """Parse the comma-separated CORS_ORIGINS env var into a list.

        In non-production, any localhost/127.0.0.1 origin is always allowed
        (dev servers move between ports), so local development never breaks.
        """
        configured = [
            origin.strip()
            for origin in self.cors_origins.split(",")
            if origin.strip()
        ]
        if not self.is_production():
            return configured  # matcher below allows localhost in dev
        return configured

    @property
    def allow_localhost_origins(self) -> bool:
        return not self.is_production()

    def is_production(self) -> bool:
        return self.environment.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    if settings.is_production():
        insecure: list[str] = []
        if settings.jwt_secret_key.startswith("dev-only"):
            insecure.append("JWT_SECRET_KEY")
        if settings.database_url.startswith("sqlite"):
            insecure.append("DATABASE_URL (sqlite is not safe for production data)")
        if insecure:
            raise RuntimeError(
                "Refusing to start in production with insecure settings: "
                + "; ".join(insecure)
            )
    return settings


settings = get_settings()
