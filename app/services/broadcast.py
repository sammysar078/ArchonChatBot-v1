import asyncio

from aiogram import Bot
from aiogram.exceptions import TelegramRetryAfter

from app.services.users import get_all_users


async def broadcast_message(bot: Bot, text: str):
    users = await get_all_users()

    success = 0
    failed = 0

    for user_id in users:
        try:
            await bot.send_message(user_id, text)
            success += 1
            await asyncio.sleep(0.05)

        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
            try:
                await bot.send_message(user_id, text)
                success += 1
            except Exception:
                failed += 1

        except Exception:
            failed += 1

    return success, failed, len(users)
