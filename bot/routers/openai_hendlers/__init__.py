__all__ = ('router', )

from aiogram import Router

from .assistant_message import router as assistant_message_router

router = Router()

router.include_routers(
    assistant_message_router,

)
