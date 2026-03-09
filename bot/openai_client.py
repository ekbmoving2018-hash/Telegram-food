"""OpenAI Responses API client for recipe generation."""

import logging
from typing import Optional

from openai import OpenAI

from bot.config import Config
from bot.prompts import RECIPE_SYSTEM_PROMPT

logger = logging.getLogger(__name__)


def _get_recipe_responses_api(client: OpenAI, config: Config, products: str) -> Optional[str]:
    """Use Responses API if available."""
    response = client.responses.create(
        model=config.openai_model,
        input=[
            {"role": "developer", "content": RECIPE_SYSTEM_PROMPT},
            {"role": "user", "content": products.strip()},
        ],
    )
    return getattr(response, "output_text", None) or None


def _get_recipe_chat_completions(client: OpenAI, config: Config, products: str) -> Optional[str]:
    """Fallback to Chat Completions API."""
    response = client.chat.completions.create(
        model=config.openai_model,
        messages=[
            {"role": "system", "content": RECIPE_SYSTEM_PROMPT},
            {"role": "user", "content": products.strip()},
        ],
    )
    choice = response.choices[0] if response.choices else None
    if choice and hasattr(choice.message, "content"):
        return choice.message.content
    return None


def get_recipe(config: Config, products: str) -> Optional[str]:
    """
    Generate recipe for given products. Uses Responses API, falls back to Chat Completions.
    Returns recipe text or None on error.
    """
    client = OpenAI(api_key=config.openai_api_key)

    try:
        if hasattr(client, "responses"):
            text = _get_recipe_responses_api(client, config, products)
        else:
            text = _get_recipe_chat_completions(client, config, products)
    except Exception as e:
        logger.exception("OpenAI API error")
        raise RuntimeError("Сервис рецептов временно недоступен. Попробуйте позже.") from e

    return text
