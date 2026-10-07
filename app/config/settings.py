"""Environment-backed application settings."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """Validated configuration loaded from environment / .env."""

    model_config = SettingsConfigDict(
        env_file=str(PROJECT_ROOT / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        populate_by_name=True,
    )

    jev_api_key: str = Field(default="", alias="JEV_API_KEY")
    jev_model: str = Field(default="jev-1.13.0", alias="JEV_MODEL")
    jev_base_url: str = Field(
        default="https://jevtypesafeai.com/api/v1/decide",
        alias="JEV_BASE_URL",
    )
    jev_timeout_seconds: float = Field(default=30.0, alias="JEV_TIMEOUT_SECONDS")

    app_env: str = Field(default="development", alias="APP_ENV")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    policy_version: str = Field(default="1.0", alias="POLICY_VERSION")

    # Deterministic policy thresholds
    auto_execute_max_risk: float = Field(default=2.0, alias="AUTO_EXECUTE_MAX_RISK")
    auto_execute_min_safe: float = Field(default=0.90, alias="AUTO_EXECUTE_MIN_SAFE")
    confirm_max_risk: float = Field(default=3.0, alias="CONFIRM_MAX_RISK")
    confirm_min_safe: float = Field(default=0.50, alias="CONFIRM_MIN_SAFE")
    block_min_risk: float = Field(default=4.0, alias="BLOCK_MIN_RISK")

    demo_workspace: Path = Field(
        default=PROJECT_ROOT / "demo" / "workspace",
        alias="DEMO_WORKSPACE",
    )

    # Outbound Jev API rate limit (live calls only; DEMO MODE is unrestricted)
    rate_limit_enabled: bool = Field(default=True, alias="RATE_LIMIT_ENABLED")
    rate_limit_max_calls: int = Field(default=3, alias="RATE_LIMIT_MAX_CALLS", ge=1)
    rate_limit_window_hours: float = Field(
        default=5.0,
        alias="RATE_LIMIT_WINDOW_HOURS",
        gt=0,
    )

    @field_validator("demo_workspace", mode="before")
    @classmethod
    def resolve_workspace(cls, value: str | Path) -> Path:
        path = Path(value)
        if not path.is_absolute():
            path = PROJECT_ROOT / path
        return path

    @field_validator("log_level")
    @classmethod
    def normalize_log_level(cls, value: str) -> str:
        level = value.upper()
        allowed = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in allowed:
            raise ValueError(f"LOG_LEVEL must be one of {sorted(allowed)}")
        return level

    @property
    def jev_configured(self) -> bool:
        return bool(self.jev_api_key.strip())

    def require_jev_api_key(self) -> str:
        key = self.jev_api_key.strip()
        if not key:
            raise ConfigError("JEV_API_KEY is not set. Copy .env.example to .env or use DEMO MODE.")
        return key


class ConfigError(Exception):
    """Raised when required configuration is missing or invalid."""


@lru_cache
def get_settings() -> Settings:
    return Settings()


def clear_settings_cache() -> None:
    get_settings.cache_clear()
