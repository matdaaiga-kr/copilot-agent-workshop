from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from ..models.models import User, Follow, Post, Like, Comment
from ..schemas.schemas import UserCreate, UserUpdate
from .auth import get_password_hash, verify_password
from typing import Optional

def create_user(db: Session, user: UserCreate):
    """새 사용자를 생성합니다"""
    # 사용자 이름 중복 확인
    db_user = db.query(User).filter(User.username == user.username).first()
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="이미 사용 중인 사용자 이름입니다"
        )

    # 비밀번호 해싱
    hashed_password = get_password_hash(user.password)
    
    # 새 사용자 생성
    db_user = User(
        username=user.username,
        hashed_password=hashed_password,
        profile_image_url=None
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, username: str, password: str):
    """사용자 인증"""
    user = db.query(User).filter(User.username == username).first()
    
    if not user:
        return False
        
    if not verify_password(password, user.hashed_password):
        return False
        
    return user

def get_user_by_id(db: Session, user_id: int):
    """ID로 사용자 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
        
    return user

def update_user(db: Session, user_id: int, user_update: UserUpdate):
    """사용자 정보 업데이트"""
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 사용자 이름 업데이트
    if user_update.username and user_update.username != db_user.username:
        # 중복 확인
        name_exists = db.query(User).filter(User.username == user_update.username).first()
        if name_exists:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미 사용 중인 사용자 이름입니다"
            )
        db_user.username = user_update.username
    
    # 프로필 이미지는 실제로는 파일 업로드 처리가 필요함
    # 여기서는 단순화를 위해 URL 문자열 저장으로 가정
    # 실제 구현 시에는 이미지 처리 미들웨어 및 스토리지 연동 필요
    
    db.commit()
    db.refresh(db_user)
    return db_user

def follow_user(db: Session, follower_id: int, followed_id: int):
    """다른 사용자 팔로우"""
    # 자기 자신을 팔로우하려는 경우 방지
    if follower_id == followed_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자기 자신을 팔로우할 수 없습니다"
        )
    
    # 팔로우할 사용자 존재 확인
    followed_user = db.query(User).filter(User.id == followed_id).first()
    if not followed_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="팔로우할 사용자를 찾을 수 없습니다"
        )
    
    # 이미 팔로우하고 있는지 확인
    existing_follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()
    
    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 팔로우하고 있는 사용자입니다"
        )
    
    # 팔로우 관계 생성
    follow = Follow(follower_id=follower_id, followed_id=followed_id)
    db.add(follow)
    db.commit()
    
    return {
        "user_id": followed_id,
        "is_following": True
    }

def unfollow_user(db: Session, follower_id: int, followed_id: int):
    """팔로우 취소"""
    # 팔로우 관계 확인
    follow = db.query(Follow).filter(
        Follow.follower_id == follower_id,
        Follow.followed_id == followed_id
    ).first()
    
    if not follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="팔로우하고 있지 않은 사용자입니다"
        )
    
    # 팔로우 관계 삭제
    db.delete(follow)
    db.commit()
    
    return {
        "user_id": followed_id,
        "is_following": False
    }

def get_user_profile(db: Session, user_id: int, current_user_id: Optional[int] = None):
    """사용자 프로필 조회"""
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 팔로워 수
    followers_count = db.query(func.count(Follow.id)).filter(
        Follow.followed_id == user_id
    ).scalar()
    
    # 팔로잉 수
    following_count = db.query(func.count(Follow.id)).filter(
        Follow.follower_id == user_id
    ).scalar()
    
    # 게시물 수
    posts_count = db.query(func.count(Post.id)).filter(
        Post.author_id == user_id
    ).scalar()
    
    # 팔로우 여부 확인
    is_following = False
    if current_user_id and current_user_id != user_id:
        follow = db.query(Follow).filter(
            Follow.follower_id == current_user_id,
            Follow.followed_id == user_id
        ).first()
        is_following = follow is not None
    
    return {
        "id": user.id,
        "username": user.username,
        "profile_image_url": user.profile_image_url,
        "followers_count": followers_count,
        "following_count": following_count,
        "posts_count": posts_count,
        "is_following": is_following,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

def get_followers(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """사용자의 팔로워 목록 조회"""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 팔로워 총 수 계산
    total = db.query(func.count(Follow.id)).filter(
        Follow.followed_id == user_id
    ).scalar()
    
    # 팔로워 목록 조회
    followers = db.query(User).join(
        Follow, Follow.follower_id == User.id
    ).filter(
        Follow.followed_id == user_id
    ).offset(skip).limit(limit).all()
    
    return followers, total

def get_following(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """사용자가 팔로우하는 목록 조회"""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 팔로잉 총 수 계산
    total = db.query(func.count(Follow.id)).filter(
        Follow.follower_id == user_id
    ).scalar()
    
    # 팔로잉 목록 조회
    following = db.query(User).join(
        Follow, Follow.followed_id == User.id
    ).filter(
        Follow.follower_id == user_id
    ).offset(skip).limit(limit).all()
    
    return following, total