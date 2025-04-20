from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import models, schemas
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException

def get_user_by_username(db: Session, username: str):
    """사용자 이름으로 사용자 검색"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int):
    """ID로 사용자 검색"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    """새 사용자 생성"""
    # 기본 프로필 이미지 URL
    default_image = "https://api.dicebear.com/7.x/avataaars/svg?seed=" + user.username
    
    db_user = models.User(
        username=user.username,
        profile_image_url=default_image
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def login_user(db: Session, username: str):
    """사용자 로그인 (없으면 새로 생성)"""
    # 기존 사용자 검색
    user = get_user_by_username(db, username)
    
    # 사용자가 없으면 새로 생성
    if not user:
        new_user = schemas.UserCreate(username=username)
        user = create_user(db, new_user)
    
    return user

def get_user_profile(db: Session, user_id: int):
    """사용자 프로필 정보 조회"""
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 게시물 수 계산
    posts_count = db.query(func.count(models.Post.id)).filter(models.Post.author_id == user_id).scalar()
    
    return user, posts_count

def search_users(db: Session, username: str, page: int, limit: int) -> Tuple[List[models.User], int]:
    """사용자 이름으로 검색"""
    # 총 사용자 수 조회 (검색어와 일치하는)
    total = db.query(func.count(models.User.id)).filter(models.User.username.ilike(f"%{username}%")).scalar()
    
    # 페이지네이션 적용한 사용자 목록 조회
    users = db.query(models.User).filter(
        models.User.username.ilike(f"%{username}%")
    ).offset((page - 1) * limit).limit(limit).all()
    
    return users, total