from aiogram import Router

from .start import router as start_router
from .chat import router as chat_router
from .voice import router as voice_router
from .memory import router as memory_router
from .admin import router as admin_router
from .maintenance import router as maintenance_router
from .broadcast import router as broadcast_router

router = Router()

# Commands first
router.include_router(start_router)
router.include_router(voice_router)
router.include_router(memory_router)
router.include_router(admin_router)
router.include_router(maintenance_router)
router.include_router(broadcast_router)

# Chat last
router.include_router(chat_router)
