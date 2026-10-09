from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Tuple


def _coerce_bool(value: str | None, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _split_csv(value: str | None, default: str = "*") -> Tuple[str, ...]:
    raw = value or default
    return tuple(part.strip() for part in raw.split(",") if part.strip())


@dataclass(frozen=True)
class Settings:
    env: str = "development"
    host: str = "0.0.0.0"
    port: int = 8000
    log_level: str = "INFO"
    debug: bool = False
    allowed_origins: Tuple[str, ...] = ("*",)
    model_base_url: str | None = None
    model_name: str | None = None
    model_api_key: str | None = None
    request_timeout_seconds: int = 120
    body_size_limit_bytes: int = 5_000_000

    @classmethod
    def from_env(cls) -> "Settings":
        env = os.getenv("H11_ENV", "development")
        allowed_origins = _split_csv(os.getenv("H11_ALLOWED_ORIGINS"), "*")

        try:
            port = int(os.getenv("PORT", os.getenv("H11_PORT", "8000")))
        except ValueError:
            port = 8000

        try:
            timeout = int(os.getenv("H11_REQUEST_TIMEOUT_SECONDS", "120"))
        except ValueError:
            timeout = 120

        try:
            body_limit = int(os.getenv("H11_BODY_SIZE_LIMIT_BYTES", str(5_000_000)))
        except ValueError:
            body_limit = 5_000_000

        return cls(
            env=env,
            host=os.getenv("HOST", os.getenv("H11_HOST", "0.0.0.0")),
            port=port,
            log_level=os.getenv("H11_LOG_LEVEL", "INFO").upper(),
            debug=_coerce_bool(os.getenv("H11_DEBUG"), False),
            allowed_origins=allowed_origins,
            model_base_url=os.getenv("H11_MODEL_BASE_URL"),
            model_name=os.getenv("H11_MODEL_NAME"),
            model_api_key=os.getenv("H11_MODEL_API_KEY"),
            request_timeout_seconds=timeout,
            body_size_limit_bytes=body_limit,
        )


def get_settings() -> Settings:
    return Settings.from_env()


__all__ = ["Settings", "get_settings"]
