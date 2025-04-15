from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.schemas.user import UserCreate, User as UserSchema, UserLogin, Token
from app.core.database import get_db
from app.core.auth import get_current_user
from app.controllers import user_controller

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)

@router.post("/signup", response_model=UserSchema)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """새 사용자 등록(회원가입)"""
    return user_controller.create_user(db=db, user=user)

@router.post("/login", response_model=Token)
def login_for_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    """로그인 및 액세스 토큰 발급"""
    user = user_controller.authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자명이나 패스워드가 올바르지 않습니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 생성
    access_token = user_controller.create_user_token(user.id)
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserSchema)
def read_user_me(current_user: User = Depends(get_current_user)):
    """현재 로그인한 사용자 정보 조회"""
    return current_user

@router.get("/{user_id}", response_model=UserSchema)
def read_user(user_id: int, db: Session = Depends(get_db)):
    """특정 사용자 정보 조회"""
    user = user_controller.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="사용자를 찾을 수 없습니다"
        )
    return user

@router.get("/{user_id}/followers", response_model=List[UserSchema])
def read_user_followers(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """특정 사용자를 팔로우하는 사용자 목록 조회"""
    followers = user_controller.get_user_followers(db, user_id, skip, limit)
    return followers

@router.get("/{user_id}/following", response_model=List[UserSchema])
def read_user_following(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """특정 사용자가 팔로우하는 사용자 목록 조회"""
    following = user_controller.get_user_following(db, user_id, skip, limit)
    return following