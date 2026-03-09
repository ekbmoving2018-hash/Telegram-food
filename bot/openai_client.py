"""OpenAI client for recipe generation."""

import logging
from typing import Optional

from openai import OpenAI
from openai import RateLimitError

from bot.config import Config
from bot.prompts import RECIPE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)
QUOTA_ERROR_MSG = (
    "Закончился лимит запросов к OpenAI. "
    "Проверьте баланс и оплату на platform.openai.com — возможно, нужно добавить способ оплаты."
)

# Models that work with Chat Completions (stable, widely available)
CHAT_MODELS = {"gpt-4o", "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo", "gpt-4"}


def _get_recipe_chat(client: OpenAI, config: Config, products: str) -> Optional[str]:
    """Use Chat Completions API (stable, works with all keys)."""
    model = config.openai_model
    if model not in CHAT_MODELS:
        model = "gpt-4o-mini"
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": RECIPE_SYSTEM_PROMPT},
            {"role": "user", "content": products.strip()},
        ],
    )
    choice = response.choices[0] if response.choices else None
    if choice and hasattr(choice.message, "content") and choice.message.content:
        return choice.message.content
    return None


def get_recipe(config: Config, products: str) -> Optional[str]:
    """
    Generate recipe for given products via OpenAI Chat Completions.
    Returns recipe text or None on error.
    """
    client = OpenAI(api_key=config.openai_api_key)

    try:
        return _get_recipe_chat(client, config, products)
    except RateLimitError as e:
        if "insufficient_quota" in str(e).lower():
            raise RuntimeError(QUOTA_ERROR_MSG) from e
        logger.exception("OpenAI rate limit: %s", str(e))
        raise RuntimeError("Слишком много запросов. Подождите минуту и попробуйте снова.") from e
    except Exception as e:
        logger.exception("OpenAI API error: %s", str(e))
        raise RuntimeError("Сервис рецептов временно недоступен. Попробуйте позже.") from e
