__all__ = ("router", )

from aiogram import Router

from .create_text_and_pic import router as create_text_and_pic_router
from .create_video import router as create_video_router
from .create_quiz_from_json import router as create_quiz_from_json_router
from .admin_menu_handler import router as admin_menu_router
from .poll import router as poll_router

router = Router(name=__name__)

router.include_router(create_text_and_pic_router)
router.include_router(create_video_router)
router.include_router(create_quiz_from_json_router)
router.include_router(admin_menu_router)
router.include_router(poll_router)
