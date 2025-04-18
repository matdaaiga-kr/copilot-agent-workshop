from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import models
from app.models.schemas import UserBase
from typing import Optional, Dict, Any, List, Tuple
import math

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """사용자명으로 사용자 조회"""
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[models.User]:
    """ID로 사용자 조회"""
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: UserBase) -> models.User:
    """사용자 생성"""
    db_user = models.User(
        username=user.username,
        profile_image_url=None  # 기본 프로필 이미지 없음
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_or_create_user(db: Session, username: str) -> models.User:
    """사용자가 존재하면 조회하고, 없으면 생성"""
    user = get_user_by_username(db, username)
    if user:
        return user
    
    # 사용자가 없으면 생성
    new_user = UserBase(username=username)
    return create_user(db, new_user)

def get_user_profile(db: Session, user_id: int) -> Optional[Dict[str, Any]]:
    """
    사용자 ID로 프로필 정보를 조회
    
    Args:
        db: 데이터베이스 세션
        user_id: 조회할 사용자 ID
    
    Returns:
        사용자 프로필 정보 또는 None (사용자가 없는 경우)
    """
    # 사용자 조회
    user = get_user_by_id(db, user_id)
    if not user:
        return None
    
    # 사용자의 게시글 목록 조회
    posts = db.query(models.Post).filter(models.Post.author_id == user_id).all()
    
    # 사용자의 댓글 목록 조회
    comments = db.query(models.Comment).filter(models.Comment.author_id == user_id).all()
    
    # 사용자의 게시글 수 조회
    posts_count = db.query(func.count(models.Post.id)).filter(models.Post.author_id == user_id).scalar()
    
    # 게시글 정보 변환
    posts_data = []
    for post in posts:
        # 게시글의 댓글 수 조회
        comments_count = db.query(func.count(models.Comment.id))\
            .filter(models.Comment.post_id == post.id)\
            .scalar()
        
        # 게시글의 좋아요 수 조회
        likes_count = db.query(func.count(models.Like.id))\
            .filter(models.Like.post_id == post.id)\
            .scalar()
        
        posts_data.append({
            "id": post.id,
            "content": post.content,
            "author": {
                "id": user.id,
                "username": user.username,
                "profile_image_url": user.profile_image_url
            },
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": False,  # 프로필 조회 시에는 is_liked 정보를 포함하지 않음
            "created_at": post.created_at,
            "updated_at": post.updated_at
        })
    
    # 댓글 정보 변환
    comments_data = []
    for comment in comments:
        comments_data.append({
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": {
                "id": user.id,
                "username": user.username,
                "profile_image_url": user.profile_image_url
            },
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        })
    
    # 결과 반환
    return {
        "id": user.id,
        "username": user.username,
        "profile_image_url": user.profile_image_url,
        "posts_count": posts_count,
        "posts": posts_data,
        "comments": comments_data,
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }

def search_users_by_username(
    db: Session, 
    username_query: str,
    skip: int = 0,
    limit: int = 10
) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    사용자명으로 사용자 검색
    
    Args:
        db: 데이터베이스 세션
        username_query: 검색할 사용자명 (부분 일치)
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
    
    Returns:
        검색 결과 사용자 목록, 전체 검색 결과 수, 전체 페이지 수
    """
    # 검색 쿼리 구성 (대소문자 구분 없이 부분 일치)
    search_term = f"%{username_query}%"
    query = db.query(models.User).filter(models.User.username.ilike(search_term))
    
    # 전체 검색 결과 수 조회
    total = query.count()
    
    # 페이지 수 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 페이지네이션 적용
    users = query.offset(skip).limit(limit).all()
    
    # 사용자 정보를 딕셔너리로 변환
    result = []
    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "profile_image_url": user.profile_image_url
        })
    
    return result, total, pages