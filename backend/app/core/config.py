from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator


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
    ENABLE_DOCS: bool = Field(default=True, description="Enable /docs and /redoc OpenAPI documentation")

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        """
        Normalize cloud provider PostgreSQL connection strings to psycopg 3 format.
        Render, Heroku, Supabase, and Railway frequently supply postgres:// or postgresql:// schemes.
        SQLAlchemy 2.0 with psycopg 3 requires postgresql+psycopg://.
        """
        if isinstance(v, str):
            if v.startswith("postgres://"):
                return v.replace("postgres://", "postgresql+psycopg://", 1)
            elif v.startswith("postgresql://") and not v.startswith("postgresql+psycopg://"):
                return v.replace("postgresql://", "postgresql+psycopg://", 1)
        return v

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if len(self.JWT_SECRET) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters long")


settings = Settings()
