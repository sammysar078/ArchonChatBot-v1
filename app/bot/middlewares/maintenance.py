from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message

from app.services.maintenance import is_maintenance
from app.services.permissions import has_permission, is_owner


class MaintenanceMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any],
    ) -> Any:
        if not is_maintenance():
            return await handler(event, data)

        user_id = event.from_user.id

        if await is_owner(user_id):
            return await handler(event, data)

        if await has_permission(user_id, "maintenance"):
            return await handler(event, data)

        await event.answer(
            "Bot is currently under maintenance. Please try again later."
        )
        return None
