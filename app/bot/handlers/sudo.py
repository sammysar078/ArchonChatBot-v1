from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import delete, select

from app.db.models import SudoUser
from app.db.session import AsyncSessionLocal
from app.services.permissions import is_owner

router = Router()

VALID_PERMISSIONS = {
    "ai",
    "groups",
    "broadcast",
    "logs",
    "voice",
    "maintenance",
    "config",
}


@router.message(Command("sudo_add"))
async def sudo_add(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Usage: /sudo_add <user_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SudoUser).where(SudoUser.user_id == user_id)
        )
        sudo = result.scalar_one_or_none()

        if sudo is None:
            session.add(SudoUser(user_id=user_id))

        await session.commit()

    await message.answer(f"User {user_id} is now a sudo user.")


@router.message(Command("sudo_remove"))
async def sudo_remove(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    parts = (message.text or "").split(maxsplit=1)
    if len(parts) != 2:
        await message.answer("Usage: /sudo_remove <user_id>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(SudoUser).where(SudoUser.user_id == user_id)
        )
        await session.commit()

    await message.answer(f"User {user_id} removed from sudo users.")


@router.message(Command("sudo_list"))
async def sudo_list(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(select(SudoUser))
        users = result.scalars().all()

    if not users:
        await message.answer("No sudo users found.")
        return

    text = "Sudo Users:\\n\\n"
    for user in users:
        text += f"• {user.user_id}\\n"

    await message.answer(text)


@router.message(Command("perm_grant"))
async def perm_grant(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    parts = (message.text or "").split(maxsplit=2)
    if len(parts) != 3:
        await message.answer("Usage: /perm_grant <user_id> <permission>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    permission = parts[2].lower()
    if permission not in VALID_PERMISSIONS:
        await message.answer("Invalid permission.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SudoUser).where(SudoUser.user_id == user_id)
        )
        sudo = result.scalar_one_or_none()

        if sudo is None:
            await message.answer("User is not a sudo user.")
            return

        setattr(sudo, permission, True)
        await session.commit()

    await message.answer(f"Granted {permission} permission to {user_id}.")


@router.message(Command("perm_revoke"))
async def perm_revoke(message: Message):
    if not await is_owner(message.from_user.id):
        await message.answer("Only owner can use this command.")
        return

    parts = (message.text or "").split(maxsplit=2)
    if len(parts) != 3:
        await message.answer("Usage: /perm_revoke <user_id> <permission>")
        return

    try:
        user_id = int(parts[1])
    except ValueError:
        await message.answer("Invalid user ID.")
        return

    permission = parts[2].lower()
    if permission not in VALID_PERMISSIONS:
        await message.answer("Invalid permission.")
        return

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SudoUser).where(SudoUser.user_id == user_id)
        )
        sudo = result.scalar_one_or_none()

        if sudo is None:
            await message.answer("User is not a sudo user.")
            return

        setattr(sudo, permission, False)
        await session.commit()

    await message.answer(f"Revoked {permission} permission from {user_id}.")
