from sqlalchemy import select

from app.config import settings
from app.db.models import SudoUser
from app.db.session import AsyncSessionLocal


async def is_owner(user_id: int) -> bool:
    return user_id == settings.OWNER_ID


async def is_sudo(user_id: int) -> bool:
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SudoUser).where(SudoUser.user_id == user_id)
        )
        return result.scalar_one_or_none() is not None


async def has_permission(user_id: int, permission: str) -> bool:
    if await is_owner(user_id):
        return True

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(SudoUser).where(SudoUser.user_id == user_id)
        )
        sudo = result.scalar_one_or_none()

        if sudo is None:
            return False

        return bool(getattr(sudo, permission, False))
