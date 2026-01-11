from pathlib import Path
from urllib.parse import urlparse

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parents[2]
ROOT_DIR = BACKEND_DIR.parent
ENV_FILES = (ROOT_DIR / ".env", BACKEND_DIR / ".env")


class Settings(BaseSettings):
    supabase_url: str
    supabase_service_key: str

    @field_validator("supabase_url")
    @classmethod
    def validate_supabase_url(cls, value: str) -> str:
        parsed = urlparse(value)
        scheme = (parsed.scheme or "").lower()
        if scheme not in {"http", "https"}:
            raise ValueError("Se requiere una URL valida de Supabase.")
        host = parsed.hostname
        if not host or host in {"localhost", "127.0.0.1", "::1"}:
            raise ValueError("Se requiere un host remoto (Supabase), no local.")
        return value

    @field_validator("supabase_service_key")
    @classmethod
    def validate_supabase_service_key(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Se requiere SUPABASE_SERVICE_KEY.")
        return value

    model_config = SettingsConfigDict(
        env_file=[str(path) for path in ENV_FILES],
        env_prefix="",
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()
