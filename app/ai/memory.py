from sqlalchemy import select

from app.db.models import UserMemory
from app.db.session import AsyncSessionLocal


async def remember(user_id: int, key: str, value: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserMemory).where(
                UserMemory.user_id == user_id,
                UserMemory.key == key,
            )
        )
        memory = result.scalar_one_or_none()

        if memory:
            memory.value = value
        else:
            session.add(
                UserMemory(
                    user_id=user_id,
                    key=key,
                    value=value,
                )
            )

        await session.commit()


async def recall(user_id: int, key: str):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(UserMemory).where(
                UserMemory.user_id == user_id,
                UserMemory.key == key,
            )
        )
        memory = result.scalar_one_or_none()

        if memory:
            return memory.value

        return None
