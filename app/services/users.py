from sqlalchemy import select

from app.db.models import User
from app.db.session import AsyncSessionLocal


async def register_user(user):
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.user_id == user.id)
        )
        existing = result.scalar_one_or_none()

        if existing is None:
            session.add(
                User(
                    user_id=user.id,
                    username=user.username or "",
                    full_name=user.full_name,
                )
            )
            await session.commit()


async def get_all_users():
    async with AsyncSessionLocal() as session:
        result = await session.execute(select(User.user_id))
        return list(result.scalars().all())
