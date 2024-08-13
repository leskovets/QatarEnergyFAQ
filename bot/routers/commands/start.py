from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import client
from openai_tool.promts import prompt_1

router = Router()


@router.message(Command('start'))
async def handler(message: Message, state: FSMContext):

    assistant = await client.beta.assistants.create(
        name="assistant",
        instructions=prompt_1['faq']['prompt'],
        model="gpt-4o",
        tools=[{"type": "file_search"}]
    )

    thread = await client.beta.threads.create()

    await state.update_data({'tread_id': thread.id})
    await state.update_data({'assistant_id': assistant.id})

    vector_store = await client.beta.vector_stores.create(name="Anxiety")

    file_paths = ["openai_tool/files/QatarEnergy.docx"]
    file_streams = [open(path, "rb") for path in file_paths]

    await client.beta.vector_stores.file_batches.upload_and_poll(
        vector_store_id=vector_store.id, files=file_streams
    )

    await client.beta.assistants.update(
        assistant_id=assistant.id,
        tool_resources={"file_search": {"vector_store_ids": [vector_store.id]}},
    )

    await message.answer(prompt_1['faq']['hello'])
