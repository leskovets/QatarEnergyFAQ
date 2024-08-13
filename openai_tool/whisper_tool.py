from config import client


async def voice_to_text(path: str) -> str:

    audio_file = open(path, "rb")
    transcription = await client.audio.transcriptions.create(
      model="whisper-1",
      file=audio_file
    )

    return transcription.text
