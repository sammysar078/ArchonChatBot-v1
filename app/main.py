import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.bot.handlers import router
from app.config import settings
from app.db.session import init_db
from app.utils.logger import logger

bot = Bot(
    token=settings.BOT_TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher()
dp.include_router(router)


async def main():
    logger.info("Initializing database...")
    await init_db()

    logger.info("Starting ArchonChatBot v1...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
