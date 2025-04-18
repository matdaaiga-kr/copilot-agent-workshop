from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import models
from app.models.schemas import PostCreate, PostUpdate
from app.controllers.user_service import get_or_create_user
from typing import List, Optional, Dict, Any, Tuple
import math
from datetime import datetime

def get_posts(
    db: Session, 
    skip: int = 0, 
    limit: int = 10, 
    current_username: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    게시글 목록을 페이지네이션하여 조회
    
    Args:
        db: 데이터베이스 세션
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
        current_username: 현재 로그인한 사용자명 (좋아요 여부 확인용)
    
    Returns:
        게시글 목록, 전체 게시글 수, 전체 페이지 수
    """
    # 전체 게시글 수 조회
    total = db.query(models.Post).count()
    
    # 페이지 수 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 게시글 목록 조회 (최신순)
    query = db.query(models.Post).order_by(desc(models.Post.created_at))
    posts = query.offset(skip).limit(limit).all()
    
    # 게시글 정보를 딕셔너리로 변환
    result = []
    for post in posts:
        # 댓글 수 조회
        comments_count = db.query(func.count(models.Comment.id))\
            .filter(models.Comment.post_id == post.id)\
            .scalar()
        
        # 좋아요 수 조회
        likes_count = db.query(func.count(models.Like.id))\
            .filter(models.Like.post_id == post.id)\
            .scalar()
        
        # 현재 사용자가 좋아요 했는지 확인
        is_liked = False
        if current_username:
            current_user = db.query(models.User)\
                .filter(models.User.username == current_username)\
                .first()
            if current_user:
                is_liked = db.query(models.Like)\
                    .filter(
                        models.Like.post_id == post.id,
                        models.Like.user_id == current_user.id
                    )\
                    .first() is not None
        
        result.append({
            "id": post.id,
            "content": post.content,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
                "profile_image_url": post.author.profile_image_url
            },
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": is_liked,
            "created_at": post.created_at,
            "updated_at": post.updated_at
        })
    
    return result, total, pages

def get_post(
    db: Session, 
    post_id: int,
    current_username: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    특정 게시글 조회
    
    Args:
        db: 데이터베이스 세션
        post_id: 조회할 게시글 ID
        current_username: 현재 로그인한 사용자명 (좋아요 여부 확인용)
    
    Returns:
        게시글 정보 또는 None
    """
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    
    if not post:
        return None
    
    # 댓글 수 조회
    comments_count = db.query(func.count(models.Comment.id))\
        .filter(models.Comment.post_id == post_id)\
        .scalar()
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(models.Like.id))\
        .filter(models.Like.post_id == post_id)\
        .scalar()
    
    # 현재 사용자가 좋아요 했는지 확인
    is_liked = False
    if current_username:
        current_user = db.query(models.User)\
            .filter(models.User.username == current_username)\
            .first()
        if current_user:
            is_liked = db.query(models.Like)\
                .filter(
                    models.Like.post_id == post_id,
                    models.Like.user_id == current_user.id
                )\
                .first() is not None
    
    return {
        "id": post.id,
        "content": post.content,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
            "profile_image_url": post.author.profile_image_url
        },
        "likes_count": likes_count,
        "comments_count": comments_count,
        "is_liked": is_liked,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

def create_post(db: Session, post: PostCreate) -> Dict[str, Any]:
    """
    게시글 생성
    
    Args:
        db: 데이터베이스 세션
        post: 게시글 생성 정보
    
    Returns:
        생성된 게시글 정보
    """
    # 사용자 확인 또는 생성
    user = get_or_create_user(db, post.username)
    
    # 게시글 생성
    db_post = models.Post(
        content=post.content,
        author_id=user.id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # 응답 형식으로 변환
    return {
        "id": db_post.id,
        "content": db_post.content,
        "author": {
            "id": user.id,
            "username": user.username,
            "profile_image_url": user.profile_image_url
        },
        "likes_count": 0,
        "comments_count": 0,
        "is_liked": False,
        "created_at": db_post.created_at,
        "updated_at": db_post.updated_at
    }

def update_post(db: Session, post_id: int, post_update: PostUpdate, username: str) -> Optional[Dict[str, Any]]:
    """
    게시글 수정
    
    Args:
        db: 데이터베이스 세션
        post_id: 수정할 게시글 ID
        post_update: 업데이트할 내용
        username: 요청한 사용자명 (작성자 확인용)
    
    Returns:
        수정된 게시글 정보 또는 None (권한 없음 또는 게시글이 없는 경우)
    """
    # 게시글 확인
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    
    # 작성자 확인
    if db_post.author.username != username:
        return None
    
    # 게시글 수정
    db_post.content = post_update.content
    db_post.updated_at = datetime.now()
    db.commit()
    db.refresh(db_post)
    
    # 수정된 게시글 조회 및 반환
    return get_post(db, post_id, username)

def delete_post(db: Session, post_id: int, username: str) -> bool:
    """
    게시글 삭제
    
    Args:
        db: 데이터베이스 세션
        post_id: 삭제할 게시글 ID
        username: 요청한 사용자명 (작성자 확인용)
    
    Returns:
        삭제 성공 여부
    """
    # 게시글 확인
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return False
    
    # 작성자 확인
    if db_post.author.username != username:
        return False
    
    # 게시글 삭제
    db.delete(db_post)
    db.commit()
    return True

def like_post(db: Session, post_id: int, username: str) -> Optional[Dict[str, Any]]:
    """
    게시글 좋아요
    
    Args:
        db: 데이터베이스 세션
        post_id: 좋아요할 게시글 ID
        username: 좋아요를 누른 사용자명
    
    Returns:
        좋아요 정보 또는 None (게시글이 없는 경우)
    """
    # 게시글 확인
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    
    # 사용자 확인
    user = get_or_create_user(db, username)
    
    # 이미 좋아요 했는지 확인
    existing_like = db.query(models.Like)\
        .filter(
            models.Like.post_id == post_id,
            models.Like.user_id == user.id
        )\
        .first()
    
    # 이미 좋아요한 경우 중복 처리 방지
    if existing_like:
        # 좋아요 수 조회
        likes_count = db.query(func.count(models.Like.id))\
            .filter(models.Like.post_id == post_id)\
            .scalar()
        
        return {
            "post_id": post_id,
            "is_liked": True,
            "likes_count": likes_count
        }
    
    # 좋아요 추가
    new_like = models.Like(
        post_id=post_id,
        user_id=user.id
    )
    db.add(new_like)
    db.commit()
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(models.Like.id))\
        .filter(models.Like.post_id == post_id)\
        .scalar()
    
    return {
        "post_id": post_id,
        "is_liked": True,
        "likes_count": likes_count
    }

def unlike_post(db: Session, post_id: int, username: str) -> Optional[Dict[str, Any]]:
    """
    게시글 좋아요 취소
    
    Args:
        db: 데이터베이스 세션
        post_id: 좋아요 취소할 게시글 ID
        username: 좋아요를 취소한 사용자명
    
    Returns:
        좋아요 취소 정보 또는 None (게시글이 없는 경우)
    """
    # 게시글 확인
    db_post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not db_post:
        return None
    
    # 사용자 확인
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user:
        return None
    
    # 좋아요 조회
    like = db.query(models.Like)\
        .filter(
            models.Like.post_id == post_id,
            models.Like.user_id == user.id
        )\
        .first()
    
    # 좋아요가 없는 경우
    if not like:
        # 좋아요 수 조회
        likes_count = db.query(func.count(models.Like.id))\
            .filter(models.Like.post_id == post_id)\
            .scalar()
        
        return {
            "post_id": post_id,
            "is_liked": False,
            "likes_count": likes_count
        }
    
    # 좋아요 삭제
    db.delete(like)
    db.commit()
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(models.Like.id))\
        .filter(models.Like.post_id == post_id)\
        .scalar()
    
    return {
        "post_id": post_id,
        "is_liked": False,
        "likes_count": likes_count
    }