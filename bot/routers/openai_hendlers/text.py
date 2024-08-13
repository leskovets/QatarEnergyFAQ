import logging

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from openai_tool.assistant_tool import get_answer_from_assistant

router = Router()
logger = logging.getLogger('text_router')


@router.message(F.text)
async def text_message_handler(message: Message, state: FSMContext):

    tread_id = (await state.get_data())['tread_id']
    assistant_id = (await state.get_data())['assistant_id']

    answer = await get_answer_from_assistant(message.text, message.chat.id, tread_id, assistant_id)
    logger.debug(f"response from the assistant: {answer}")

    await message.answer(text=answer)
