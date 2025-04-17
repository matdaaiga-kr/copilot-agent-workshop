from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..models.database import get_db
from ..models.models import User
from ..schemas.schemas import UserProfile, UserList, PostList, PaginationParams
from ..services.auth import get_current_user
from ..services.user import get_user_profile, get_followers, get_following
from ..services.post import get_user_posts

router = APIRouter(
    prefix="/profile",
    tags=["프로필"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "인증되지 않은 사용자"},
        status.HTTP_404_NOT_FOUND: {"description": "찾을 수 없는 리소스"}
    }
)

@router.get("/me", response_model=UserProfile)
async def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 프로필 조회"""
    return get_user_profile(db, current_user.id, current_user.id)

@router.get("/me/posts", response_model=PostList)
async def get_my_posts(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=50, description="페이지당 항목 수"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 게시물 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    return get_user_posts(db, current_user.id, current_user.id, pagination)

@router.get("/me/followers", response_model=UserList)
async def get_my_followers(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내 팔로워 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    followers, total = get_followers(db, current_user.id, pagination.skip, pagination.limit)
    
    # 팔로워 프로필 정보 조회
    followers_with_profile = []
    for follower in followers:
        profile = get_user_profile(db, follower.id, current_user.id)
        followers_with_profile.append(profile)
    
    # 페이지네이션 정보
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0
    
    return {
        "items": followers_with_profile,
        "total": total,
        "page": pagination.page,
        "size": pagination.limit,
        "pages": pages
    }

@router.get("/me/following", response_model=UserList)
async def get_my_following(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """내가 팔로우하는 사용자 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    following, total = get_following(db, current_user.id, pagination.skip, pagination.limit)
    
    # 팔로잉 프로필 정보 조회
    following_with_profile = []
    for follow in following:
        profile = get_user_profile(db, follow.id, current_user.id)
        following_with_profile.append(profile)
    
    # 페이지네이션 정보
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0
    
    return {
        "items": following_with_profile,
        "total": total,
        "page": pagination.page,
        "size": pagination.limit,
        "pages": pages
    }

@router.get("/{user_id}", response_model=UserProfile)
async def get_user_profile_endpoint(
    user_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """특정 사용자 프로필 조회"""
    current_user_id = current_user.id if current_user else None
    return get_user_profile(db, user_id, current_user_id)