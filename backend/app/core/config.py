from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, ValidationError


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    DATABASE_URL: str = Field(
        default="postgresql+psycopg://snackoverflow:snackoverflow@localhost:5432/snackoverflow",
        description="PostgreSQL database URL"
    )
    JWT_SECRET: str = Field(..., description="JWT secret key (must be at least 32 characters)")
    JWT_ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="Access token expiration in minutes")
    CORS_ORIGINS: str = Field(default="http://localhost:5173", description="Comma-separated CORS origins")
    ENV: str = Field(default="development", description="Environment (development/production)")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if len(self.JWT_SECRET) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")


settings = Settings()
