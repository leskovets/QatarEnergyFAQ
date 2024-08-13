from openai import AsyncOpenAI
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    API_TOKEN_OPENAI: str
    API_TOKEN_TELEGRAM: str
    REDIS_URL: str
    ASSISTANT_ID: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()

client = AsyncOpenAI(api_key=settings.API_TOKEN_OPENAI)
