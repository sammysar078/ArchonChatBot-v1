from openai import AsyncOpenAI

from app.ai.context import (
    add_assistant_message,
    add_user_message,
    get_context,
)
from app.ai.group_context import (
    add_group_assistant_message,
    add_group_user_message,
    get_group_context,
)
from app.ai.prompts import SYSTEM_PROMPT
from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def generate_reply(user_id: int, user_message: str) -> str:
    return await generate_private_reply(user_id, user_message)


async def generate_private_reply(user_id: int, user_message: str) -> str:
    if not settings.OPENAI_API_KEY:
        return (
            "OpenAI API key configured nahi hai.\\n"
            "Abhi placeholder mode mein chal raha hoon."
        )

    try:
        add_user_message(user_id, user_message)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_context(user_id))

        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.8,
        )

        reply = response.choices[0].message.content.strip()

        add_assistant_message(user_id, reply)

        return reply

    except Exception:
        return "AI service se connect nahi ho pa raha. Baad mein dobara try karo."


async def generate_group_reply(chat_id: int, user_message: str) -> str:
    if not settings.OPENAI_API_KEY:
        return (
            "OpenAI API key configured nahi hai.\\n"
            "Abhi placeholder mode mein chal raha hoon."
        )

    try:
        add_group_user_message(chat_id, user_message)

        messages = [{"role": "system", "content": SYSTEM_PROMPT}]
        messages.extend(get_group_context(chat_id))

        response = await client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
            temperature=0.8,
        )

        reply = response.choices[0].message.content.strip()

        add_group_assistant_message(chat_id, reply)

        return reply

    except Exception:
        return "AI service se connect nahi ho pa raha. Baad mein dobara try karo."
