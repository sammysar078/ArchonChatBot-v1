from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

from app.services.users import register_user

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await register_user(message.from_user)

    await message.answer(
        "Hello! I am <b>ArchonChatBot v1</b>.\\n\\n"
        "Main multilingual AI companion hoon. Mujhse Hindi, Hinglish, English, Indonesian ya kisi aur language mein baat kar sakte ho."
    )


@router.message(Command("help"))
async def help_command(message: Message):
    await message.answer(
        "/start - Start the bot\\n"
        "/help - Show help\\n"
        "/ping - Check if bot is online"
    )


@router.message(Command("ping"))
async def ping(message: Message):
    await message.answer("Pong! ArchonChatBot v1 is online.")
