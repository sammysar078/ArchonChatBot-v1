from pathlib import Path

from openai import AsyncOpenAI

from app.config import settings

client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


async def transcribe_voice(file_path: str) -> str:
    if not settings.OPENAI_API_KEY:
        return ""

    path = Path(file_path)

    try:
        with path.open("rb") as audio:
            result = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio,
            )
        return result.text
    except Exception:
        return ""
