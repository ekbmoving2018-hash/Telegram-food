"""FastAPI app with webhook for Telegram bot."""

import asyncio
import logging
import sys
from contextlib import asynccontextmanager

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import Update
from fastapi import FastAPI, Request

from bot.config import Config
from bot.handlers import setup_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)
logger = logging.getLogger(__name__)


def _create_app(config: Config) -> tuple[Bot, Dispatcher, FastAPI]:
    """Create bot, dispatcher and FastAPI app."""
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()
    dp.include_router(setup_router(config))

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        webhook_url = f"{config.webhook_base_url}{config.webhook_path}"

        async def set_webhook_task():
            try:
                await bot.set_webhook(webhook_url)
                logger.info("Webhook set: %s", webhook_url)
            except Exception as e:
                logger.exception("Failed to set webhook: %s", e)

        asyncio.create_task(set_webhook_task())
        yield
        try:
            await bot.delete_webhook()
        except Exception as e:
            logger.warning("Failed to delete webhook: %s", e)

    app = FastAPI(lifespan=lifespan)

    @app.post(config.webhook_path)
    async def webhook(request: Request):
        try:
            data = await request.json()
            update = Update.model_validate(data)
            await dp.feed_webhook_update(bot, update)
        except Exception as e:
            logger.exception("Webhook error: %s", e)
        return {"ok": True}

    @app.get("/")
    async def root():
        return {"status": "ok", "service": "telegram-recipe-bot"}

    return bot, dp, app


try:
    _config = Config.from_env()
except ValueError as e:
    logging.getLogger(__name__).error("Config error: %s", e)
    sys.exit(1)

_bot, _dp, app = _create_app(_config)
app.state.bot = _bot
app.state.dp = _dp


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=_config.port,
        reload=False,
    )
