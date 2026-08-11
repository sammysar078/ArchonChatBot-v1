from aiogram import Bot

from app.config import settings


async def log_event(bot: Bot, text: str):
    if settings.LOGGER_GROUP_ID == 0:
        return

    try:
        await bot.send_message(settings.LOGGER_GROUP_ID, text)
    except Exception:
        pass
