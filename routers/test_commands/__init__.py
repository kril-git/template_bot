__all__ = ("router", )

from aiogram import Router

from .test_quiz import router as test_quiz_router

router = Router(name=__name__)

router.include_router(test_quiz_router)
