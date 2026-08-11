from aiogram import Router
from aiogram.types import Message

from app.ai.provider import generate_group_reply

router = Router()

GREETINGS = {
    "hi",
    "hello",
    "hey",
    "namaste",
    "assalamualaikum",
    "assalamu alaikum",
    "salam",
}


@router.message()
async def group_chat(message: Message):
    if message.chat.type == "private":
        return

    text = (message.text or "").strip()
    if not text:
        return

    bot_info = await message.bot.get_me()

    should_reply = False

    # Mention
    if f"@{bot_info.username}".lower() in text.lower():
        should_reply = True

    # Reply to bot
    if (
        message.reply_to_message
        and message.reply_to_message.from_user
        and message.reply_to_message.from_user.id == bot_info.id
    ):
        should_reply = True

    # Greeting
    if text.lower() in GREETINGS:
        should_reply = True

    if not should_reply:
        return

    cleaned = text.replace(f"@{bot_info.username}", "").strip()
    if not cleaned:
        cleaned = text

    reply = await generate_group_reply(message.chat.id, cleaned)
    await message.reply(reply)
