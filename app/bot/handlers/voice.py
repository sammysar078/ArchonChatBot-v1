import os
import tempfile

from aiogram import Router
from aiogram.types import FSInputFile, Message

from app.ai.provider import generate_reply
from app.services.users import is_voice_enabled
from app.voice.stt import transcribe_voice
from app.voice.tts import generate_voice

router = Router()


@router.message(lambda message: message.voice is not None)
async def voice_message(message: Message):
    temp_dir = tempfile.gettempdir()
    input_path = os.path.join(temp_dir, f"{message.voice.file_id}.ogg")
    output_path = os.path.join(temp_dir, f"{message.voice.file_id}.mp3")

    file = await message.bot.get_file(message.voice.file_id)
    await message.bot.download_file(file.file_path, destination=input_path)

    text = await transcribe_voice(input_path)

    if not text:
        await message.answer(
            "Voice message samajh nahi paaya. Dobara try karo."
        )
        return

    reply = await generate_reply(message.from_user.id, text)

    use_voice_reply = await is_voice_enabled(message.from_user.id)

    if use_voice_reply:
        ok = await generate_voice(reply, output_path)
        if ok:
            await message.answer_voice(FSInputFile(output_path))
        else:
            await message.answer(reply)
    else:
        await message.answer(reply)

    for path in (input_path, output_path):
        try:
            os.remove(path)
        except Exception:
            pass
