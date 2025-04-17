from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .posts import router as posts_router
from .comments import router as comments_router
from .profile import router as profile_router

router = APIRouter()

# 라우터 등록
router.include_router(auth_router)
router.include_router(users_router)
router.include_router(posts_router)
router.include_router(comments_router)
router.include_router(profile_router)