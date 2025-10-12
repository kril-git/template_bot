__all__ = ("router", )

from aiogram import Router

from handlers.base_commands import router as base_commands_router
from handlers.registration_commands import router as registration_commands_router

router = Router(name=__name__)


router.include_router(registration_commands_router)
router.include_router(base_commands_router)