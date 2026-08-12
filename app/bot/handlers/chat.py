from aiogram import Router
from aiogram.types import Message

from app.ai.provider import generate_reply
from app.services.users import register_user

router = Router()


@router.message()
async def chat(message: Message):
    if message.chat.type != "private":
        return

    if message.text and message.text.startswith("/"):
        return

    text = message.text or message.caption
    if not text:
        return

    try:
        await register_user(message.from_user)
    except Exception:
        pass

    reply = await generate_reply(message.from_user.id, text)
    await message.answer(reply)
