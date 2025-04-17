from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..models.database import get_db
from ..models.models import User
from ..schemas.schemas import UserProfile, UserUpdate, FollowResponse, UserList, PaginationParams
from ..services.auth import get_current_user
from ..services.user import get_user_profile, follow_user, unfollow_user, get_followers, get_following, update_user

router = APIRouter(
    prefix="/users",
    tags=["사용자"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "인증되지 않은 사용자"},
        status.HTTP_404_NOT_FOUND: {"description": "찾을 수 없는 리소스"}
    }
)

@router.get("/me", response_model=UserProfile)
async def read_users_me(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 로그인한 사용자 정보 조회"""
    return get_user_profile(db, current_user.id, current_user.id)

@router.put("/me", response_model=UserProfile)
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """현재 로그인한 사용자 정보 수정"""
    updated_user = update_user(db, current_user.id, user_update)
    return get_user_profile(db, current_user.id, current_user.id)

@router.get("/{user_id}", response_model=UserProfile)
async def read_user(
    user_id: int, 
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """특정 사용자 프로필 조회"""
    return get_user_profile(db, user_id, current_user.id)

@router.post("/{user_id}/follow", response_model=FollowResponse)
async def follow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 팔로우"""
    return follow_user(db, current_user.id, user_id)

@router.delete("/{user_id}/follow", response_model=FollowResponse)
async def unfollow(
    user_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자 언팔로우"""
    return unfollow_user(db, current_user.id, user_id)

@router.get("/{user_id}/followers", response_model=UserList)
async def read_followers(
    user_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자의 팔로워 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    followers, total = get_followers(db, user_id, pagination.skip, pagination.limit)
    
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

@router.get("/{user_id}/following", response_model=UserList)
async def read_following(
    user_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """사용자가 팔로우하는 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    following, total = get_following(db, user_id, pagination.skip, pagination.limit)
    
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