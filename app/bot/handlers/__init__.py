from aiogram import Router

from .start import router as start_router
from .chat import router as chat_router

router = Router()
router.include_router(start_router)
router.include_router(chat_router)
