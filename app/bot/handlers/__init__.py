from aiogram import Router

from .start import router as start_router
from .memory import router as memory_router
from .admin import router as admin_router
from .group import router as group_router
from .chat import router as chat_router

router = Router()
router.include_router(start_router)
router.include_router(memory_router)
router.include_router(admin_router)
router.include_router(group_router)
router.include_router(chat_router)
