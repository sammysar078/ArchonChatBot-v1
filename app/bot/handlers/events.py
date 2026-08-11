from aiogram import Router
from aiogram.types import ChatMemberUpdated

from app.services.logger import log_event

router = Router()


@router.my_chat_member()
async def bot_membership_changed(event: ChatMemberUpdated):
    chat = event.chat
    old_status = event.old_chat_member.status
    new_status = event.new_chat_member.status

    if old_status in {"left", "kicked"} and new_status in {
        "member",
        "administrator",
    }:
        await log_event(
            event.bot,
            (
                "➕ <b>Bot Added to Group</b>\\n\\n"
                f"<b>Group:</b> {chat.title}\\n"
                f"<b>Group ID:</b> <code>{chat.id}</code>\\n"
                f"<b>By:</b> {event.from_user.full_name} (@{event.from_user.username or 'N/A'})"
            ),
        )

    elif old_status in {"member", "administrator"} and new_status in {
        "left",
        "kicked",
    }:
        await log_event(
            event.bot,
            (
                "➖ <b>Bot Removed from Group</b>\\n\\n"
                f"<b>Group:</b> {chat.title}\\n"
                f"<b>Group ID:</b> <code>{chat.id}</code>\\n"
                f"<b>By:</b> {event.from_user.full_name} (@{event.from_user.username or 'N/A'})"
            ),
        )
