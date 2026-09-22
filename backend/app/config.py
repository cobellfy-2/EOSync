"""Zentrale Konfiguration, geladen aus Umgebungsvariablen / .env.

Lernziel: Secrets und Umgebungs-Unterschiede gehoeren NIE in den Code.
pydantic-settings liest .env und validiert die Typen beim Start.
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_env: str = "development"
    log_level: str = "INFO"

    # NCBI (PubMed, GEO)
    ncbi_api_key: str = ""
    ncbi_tool_name: str = "eosync"
    ncbi_admin_email: str = ""

    # Cache
    redis_url: str = ""
    cache_ttl_seconds: int = 86_400

    # CORS: kommaseparierte Liste
    cors_origins: str = "http://localhost:5173"

    @property
    def cors_origin_list(self) -> list[str]:
        return [o.strip() for o in self.cors_origins.split(",") if o.strip()]

    @property
    def ncbi_rate_limit(self) -> int:
        """NCBI erlaubt 3 req/s ohne Key, 10 req/s mit Key."""
        return 10 if self.ncbi_api_key else 3


@lru_cache
def get_settings() -> Settings:
    """Gecached, damit .env nur einmal pro Prozess gelesen wird."""
    return Settings()
