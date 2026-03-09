"""Configuration from environment variables."""

from dataclasses import dataclass
from os import getenv
from urllib.parse import urlparse


def _normalize_webhook_base(url: str) -> str:
    """Ensure base URL has no path. Telegram requires https://domain.com format."""
    parsed = urlparse(url)
    base = f"{parsed.scheme or 'https'}://{parsed.netloc}" if parsed.netloc else url
    return base.rstrip("/")


def _normalize_webhook_path(path: str) -> str:
    """Ensure path starts with / and has no protocol."""
    path = (path or "").strip()
    if path.startswith("http://") or path.startswith("https://"):
        parsed = urlparse(path)
        path = parsed.path or "/webhook"
    if not path.startswith("/"):
        path = "/" + path
    return path if path != "/" else "/webhook"


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
        webhook_base = getenv("WEBHOOK_BASE_URL")
        if not webhook_base:
            railway_domain = getenv("RAILWAY_PUBLIC_DOMAIN")
            if railway_domain:
                webhook_base = f"https://{railway_domain}"
            else:
                raise ValueError("WEBHOOK_BASE_URL or RAILWAY_PUBLIC_DOMAIN is required")

        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")

        webhook_path = _normalize_webhook_path(getenv("WEBHOOK_PATH", "/webhook"))
        webhook_base = _normalize_webhook_base(webhook_base)

        return cls(
            telegram_bot_token=token,
            openai_api_key=api_key,
            openai_model=getenv("OPENAI_MODEL", "gpt-4o-mini"),
            webhook_base_url=webhook_base,
            webhook_path=webhook_path,
            port=int(getenv("PORT", "8000")),
        )
