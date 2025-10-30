__all__ = ("router", )

from aiogram import Router

# from handlers import router as commands_router
# from handlers.handlers import router as handlers_router
from .admin_commands import router as admin_router
from middleware import router as outer_middleware
from .test_commands import router as test_quiz_router

router = Router(name=__name__)

router.include_routers(outer_middleware,
                       # handlers_router,
                       admin_router,
                       test_quiz_router,
                       # commands_router,
                       )
