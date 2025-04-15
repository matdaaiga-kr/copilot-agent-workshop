from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.user import User
from app.models.follower import Follower
from app.schemas.user import UserCreate
from app.core.auth import get_password_hash, verify_password, create_access_token
from datetime import timedelta
from app.core.config import settings

def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()

def create_user(db: Session, user: UserCreate):
    # 이미 존재하는 사용자인지 확인
    db_user = get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="이미 등록된 사용자 이름입니다."
        )
    
    # 비밀번호 해싱
    hashed_password = get_password_hash(user.password)
    
    # 새 사용자 생성
    db_user = User(
        username=user.username,
        hashed_password=hashed_password
    )
    
    # DB에 사용자 저장
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    
    # 사용자가 없거나 비밀번호가 일치하지 않음
    if not user or not verify_password(password, user.hashed_password):
        return False
    
    return user

def create_user_token(user_id: int):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return create_access_token(
        data={"sub": str(user_id)}, 
        expires_delta=access_token_expires
    )

def get_user_followers(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """해당 사용자를 팔로우하는 사람들 목록 조회"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    # 해당 사용자를 팔로우하는 사용자 목록 조회
    followers = db.query(User)\
        .join(Follower, Follower.follower_id == User.id)\
        .filter(Follower.following_id == user_id)\
        .offset(skip).limit(limit).all()
    
    return followers

def get_user_following(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """해당 사용자가 팔로우하는 사람들 목록 조회"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다."
        )
    
    # 해당 사용자가 팔로우하는 사용자 목록 조회
    following = db.query(User)\
        .join(Follower, Follower.following_id == User.id)\
        .filter(Follower.follower_id == user_id)\
        .offset(skip).limit(limit).all()
    
    return following