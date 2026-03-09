"""Bot message handlers."""

import logging
from functools import partial

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from bot.config import Config
from bot.openai_client import get_recipe

logger = logging.getLogger(__name__)
router = Router()

MIN_PRODUCTS_LEN = 2


async def start_handler(message: Message) -> None:
    """Handle /start command."""
    name = message.from_user.full_name if message.from_user else "Пользователь"
    await message.answer(
        f"Привет, {hbold(name)}!\n\n"
        "Пришли список продуктов, и я предложу, что из них приготовить.\n\n"
        "Например: яйца, сыр, помидоры, хлеб",
        parse_mode="HTML",
    )


async def text_handler(message: Message, config: Config) -> None:
    """Handle text message with products list."""
    text = (message.text or "").strip()

    if len(text) < MIN_PRODUCTS_LEN:
        await message.answer(
            "Пришлите список продуктов через запятую.\n"
            "Например: яйца, сыр, помидоры, хлеб",
        )
        return

    await message.bot.send_chat_action(message.chat.id, "typing")
    try:
        recipe = get_recipe(config, text)
    except RuntimeError as e:
        logger.warning("Recipe generation failed: %s", e)
        await message.answer(str(e))
        return
    except Exception as e:
        logger.exception("Unexpected error in get_recipe")
        await message.answer("Произошла ошибка. Попробуйте позже.")
        return

    if not recipe:
        await message.answer("Не удалось сгенерировать рецепт. Попробуйте позже.")
        return

    # Escape HTML for Telegram
    recipe_safe = recipe.replace("<", "&lt;").replace(">", "&gt;")
    await message.answer(recipe_safe, parse_mode="HTML")


def setup_router(config: Config) -> Router:
    """Register handlers and return router."""
    router.message.register(start_handler, CommandStart())
    router.message.register(
        partial(text_handler, config=config),
        F.text,
    )
    return router
