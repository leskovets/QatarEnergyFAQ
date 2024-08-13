from config import client


async def text_in_voice(text: str, path: str) -> None:

    response = await client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text,
    )

    response.stream_to_file(path)
