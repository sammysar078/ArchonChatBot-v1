from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.logger import log_event
from app.services.permissions import is_owner, is_sudo

router = Router()


@router.message(Command("whoami"))
async def whoami(message: Message):
    if await is_owner(message.from_user.id):
        await message.answer("You are the <b>Owner</b> of ArchonChatBot v1.")
    elif await is_sudo(message.from_user.id):
        await message.answer("You are a <b>Sudo User</b>.")
    else:
        await message.answer("You are a normal user.")


@router.message(Command("logtest"))
async def logtest(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    await log_event(message.bot, "🧪 Logger test from ArchonChatBot v1")
    await message.answer("Test log sent to logger group.")
