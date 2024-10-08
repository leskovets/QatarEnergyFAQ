from openai import AsyncOpenAI
from aiogram import Bot
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TOKEN_OPENAI: str
    API_TOKEN_TELEGRAM: str
    REDIS_URL: str
    ASSISTANT_ID: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

bot = Bot(settings.API_TOKEN_TELEGRAM)

client = AsyncOpenAI(api_key=settings.API_TOKEN_OPENAI)
