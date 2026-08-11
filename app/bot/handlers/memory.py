from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from sqlalchemy import delete, select

from app.db.models import UserMemory
from app.db.session import AsyncSessionLocal

router = Router()


@router.message(Command("memory"))
async def memory(message: Message):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserMemory).where(UserMemory.user_id == message.from_user.id)
        )
        memories = result.scalars().all()

        if not memories:
            await message.answer("Mere paas tumhari koi saved memory nahi hai.")
            return

        text = "Tumhari saved memories:\\n\\n"
        for m in memories:
            text += f"• {m.key}: {m.value}\\n"

        await message.answer(text)


@router.message(Command("forget"))
async def forget(message: Message):
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(UserMemory).where(
                UserMemory.user_id == message.from_user.id,
                UserMemory.key == "name",
            )
        )
        await session.commit()

    await message.answer("Theek hai, maine tumhara saved naam bhool diya.")


@router.message(Command("forgetall"))
async def forget_all(message: Message):
    async with AsyncSessionLocal() as session:
        await session.execute(
            delete(UserMemory).where(UserMemory.user_id == message.from_user.id)
        )
        await session.commit()

    await message.answer("Maine tumhari saari saved memories delete kar di.")
