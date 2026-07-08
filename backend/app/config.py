import os
from pathlib import Path
from typing import Optional
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from urllib.parse import unquote

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Email configuration (simulated for dev)
    EMAIL_LOG_FILE: str = str(BASE_DIR / "email_dispatch.log")

    # Real SMTP configuration
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    SMTP_FROM_NAME: str = "Acme IT Operations"

    @field_validator("DATABASE_URL", mode="after")
    @classmethod
    def decode_database_name(cls, v: str) -> str:
        """Unquotes the database name portion of the connection string to handle spaces."""
        if "/" in v:
            parts = v.rsplit("/", 1)
            # Only unquote the database name part (after the last '/') to avoid messing up password special characters like %40
            return parts[0] + "/" + unquote(parts[1])
        return v

    # Load from the correct absolute path to .env file
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()

