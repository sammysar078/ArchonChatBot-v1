from aiogram import Router
from aiogram.types import Message

from app.ai.provider import generate_reply
from app.services.users import register_user

router = Router()


@router.message()
async def chat(message: Message):
    # Ignore commands
    if message.text and message.text.startswith("/"):
        return

    # Register user
    await register_user(message.from_user)

    text = message.text or message.caption
    if not text:
        return

    try:
        reply = await generate_reply(message.from_user.id, text)
    except Exception:
        reply = "Mujhe AI response generate karne mein problem aa rahi hai. Thodi der baad try karo."

    await message.answer(reply)
