import asyncio
import os
import logging
from datetime import datetime

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, FSInputFile

from openai_tool.tts_tool import text_in_voice
from openai_tool.assistant_tool import get_answer_from_assistant
from openai_tool.whisper_tool import voice_to_text
from config import settings, bot

router = Router()
logger = logging.getLogger('voice_router')


class CustomSendVoice:
    def __init__(self, tg_id: int, state):
        self.bot = bot
        self.tg_id = tg_id
        self.loop_task = None
        self.running = False
        self.state_obj = state

    async def __aenter__(self):
        self.state = await self.state_obj.get_state()
        await self.state_obj.set_state("UserStates:no_more_messages")

        self.running = True
        self.loop_task = asyncio.create_task(self.typing_loop())

    async def typing_loop(self):
        while self.running:
            try:
                await self.bot.send_chat_action(chat_id=self.tg_id, action="record_voice")
                await asyncio.sleep(5)
            except Exception as x:
                logger.exception(x)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.loop_task:
            try:
                await self.loop_task  # Await task to handle normal completion
            except asyncio.CancelledError:
                pass
        await self.state_obj.set_state(self.state)


class CustomSendAction:
    def __init__(self, tg_id: int, state):
        self.bot = bot
        self.tg_id = tg_id
        self.loop_task = None
        self.running = False
        self.state_obj = state

    async def __aenter__(self):
        self.state = await self.state_obj.get_state()
        await self.state_obj.set_state("UserStates:no_more_messages")

        self.running = True
        self.loop_task = asyncio.create_task(self.typing_loop())

    async def typing_loop(self):
        while self.running:
            try:
                await self.bot.send_chat_action(chat_id=self.tg_id, action="typing")
                await asyncio.sleep(5)
            except Exception as x:
                logger.exception(x)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.running = False
        if self.loop_task:
            try:
                await self.loop_task  # Await task to handle normal completion
            except asyncio.CancelledError:
                pass
        await self.state_obj.set_state(self.state)


class UserStates(StatesGroup):
    no_more_messages = State()


@router.message(F.voice)
async def voice_handler(message: Message, state: FSMContext):
    try:
        async with CustomSendVoice(tg_id=message.from_user.id, state=state):
            file_id = message.voice.file_id
            file = await message.bot.get_file(file_id)
            file_path = file.file_path
            file_name = f"{message.chat.id}_{datetime.now()}.mp3"

            await message.bot.download_file(file_path, file_name)
            logger.debug(f"download_audio complete, filename: '{file_name}'")

            text = await voice_to_text(file_name)
            logger.debug(f"converting from sound to text: {text}")

            tread_id = (await state.get_data())['tread_id']

            answer = await get_answer_from_assistant(text, message.chat.id, tread_id, settings.ASSISTANT_ID)
            logger.debug(f"response from the assistant: {answer}")

            await text_in_voice(answer, file_name)
            logger.debug(f"convert text to sound")

            image_from_pc = FSInputFile(file_name)

            await message.reply_voice(image_from_pc)

            logger.debug(f"send voice to user")
            os.remove(file_name)
    except Exception as ex:
        await message.answer('something went wrong, repeat the input')


@router.message(F.text)
async def text_message_handler(message: Message, state: FSMContext):
    try:
        async with CustomSendAction(tg_id=message.from_user.id, state=state):

            tread_id = (await state.get_data())['tread_id']

            answer = await get_answer_from_assistant(message.text, message.chat.id, tread_id, settings.ASSISTANT_ID)
            logger.debug(f"response from the assistant: {answer}")
            try:
                await message.answer(text=answer, parse_mode="Markdown")
            except Exception as ex:
                await message.answer(text=answer)

    except Exception as ex:
        await message.answer('something went wrong, repeat the input')