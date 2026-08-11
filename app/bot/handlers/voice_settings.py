from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.users import (
    set_voice_enabled,
    is_voice_enabled,
)

router = Router()


@router.message(Command("voice_on"))
async def voice_on(message: Message):
    await set_voice_enabled(message.from_user.id, True)
    await message.answer(
        "Voice mode enabled. Ab main female voice mein reply de sakta hoon."
    )


@router.message(Command("voice_off"))
async def voice_off(message: Message):
    await set_voice_enabled(message.from_user.id, False)
    await message.answer("Voice mode disabled.")


@router.message(Command("voice"))
async def voice_status(message: Message):
    enabled = await is_voice_enabled(message.from_user.id)
    status = "ON" if enabled else "OFF"
    await message.answer(f"Voice mode: {status}")
