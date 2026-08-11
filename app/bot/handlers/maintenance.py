from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from app.services.maintenance import (
    is_maintenance,
    set_maintenance,
)
from app.services.permissions import (
    has_permission,
    is_owner,
)

router = Router()


@router.message(Command("maintenance_on"))
async def maintenance_on(message: Message):
    user_id = message.from_user.id

    if not (
        await is_owner(user_id)
        or await has_permission(user_id, "maintenance")
    ):
        await message.answer("Permission denied.")
        return

    set_maintenance(True)
    await message.answer("Maintenance mode enabled.")


@router.message(Command("maintenance_off"))
async def maintenance_off(message: Message):
    user_id = message.from_user.id

    if not (
        await is_owner(user_id)
        or await has_permission(user_id, "maintenance")
    ):
        await message.answer("Permission denied.")
        return

    set_maintenance(False)
    await message.answer("Maintenance mode disabled.")


@router.message(Command("maintenance"))
async def maintenance_status(message: Message):
    status = "ON" if is_maintenance() else "OFF"
    await message.answer(f"Maintenance mode: {status}")
