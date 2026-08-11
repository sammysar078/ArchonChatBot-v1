from aiogram import Router
from aiogram.types import Message

from app.ai.provider import generate_reply

router = Router()


@router.message()
async def chat(message: Message):
    if message.chat.type != "private":
        return

    if not message.text:
        await message.answer("I can understand text messages for now.")
        return

    reply = await generate_reply(message.from_user.id, message.text)
    await message.answer(reply)
