from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import client
from openai_tool.crate_assistant import create_assistant
from openai_tool.promts import prompt_1

router = Router()


@router.message(Command('start'))
async def start(message: Message, state: FSMContext):

    thread = await client.beta.threads.create()
    await state.update_data({'tread_id': thread.id})

    await message.answer(prompt_1['faq']['hello'])


@router.message(Command('create_assistant'))
async def create(message: Message):

    assistant_id = await create_assistant()

    await message.answer(assistant_id)

