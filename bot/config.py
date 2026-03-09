"""Configuration from environment variables."""

from dataclasses import dataclass
from os import getenv


@dataclass(frozen=True)
class Config:
    """App configuration."""

    telegram_bot_token: str
    openai_api_key: str
    openai_model: str
    webhook_base_url: str
    webhook_path: str
    port: int

    @classmethod
    def from_env(cls) -> "Config":
        """Load config from environment. Raises ValueError if required vars missing."""
        token = getenv("TELEGRAM_BOT_TOKEN")
        api_key = getenv("OPENAI_API_KEY")
        webhook_url = getenv("WEBHOOK_BASE_URL")
        if not webhook_url:
            railway_domain = getenv("RAILWAY_PUBLIC_DOMAIN")
            if railway_domain:
                webhook_url = f"https://{railway_domain}"
            else:
                raise ValueError("WEBHOOK_BASE_URL or RAILWAY_PUBLIC_DOMAIN is required")

        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        return cls(
            telegram_bot_token=token,
            openai_api_key=api_key,
            openai_model=getenv("OPENAI_MODEL", "gpt-4.1"),
            webhook_base_url=webhook_url.rstrip("/"),
            webhook_path=getenv("WEBHOOK_PATH", "/webhook"),
            port=int(getenv("PORT", "8000")),
        )
