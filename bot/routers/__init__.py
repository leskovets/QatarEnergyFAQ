__all__ = ('router', )

from aiogram import Router

from .commands import router as commands_router
from .openai_hendlers import router as openai_router

router = Router()

router.include_routers(
    commands_router,
    openai_router,

)
