from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

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
