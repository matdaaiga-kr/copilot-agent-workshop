from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import models, schemas
from app.controllers import user_service
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException
import math

def get_post(db: Session, post_id: int):
    """ID로 게시물 조회"""
    return db.query(models.Post).filter(models.Post.id == post_id).first()

def create_post(db: Session, post: schemas.PostCreate):
    """새 게시물 생성"""
    # 작성자 확인 또는 생성
    user = user_service.get_user_by_username(db, post.username)
    if not user:
        user_data = schemas.UserCreate(username=post.username)
        user = user_service.create_user(db, user_data)
    
    # 새 게시물 생성
    db_post = models.Post(
        content=post.content,
        author_id=user.id
    )
    
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int, username: str):
    """게시물 삭제"""
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user or post.author_id != user.id:
        raise HTTPException(status_code=401, detail="Not authorized to delete this post")
    
    db.delete(post)
    db.commit()
    return {"message": "Post deleted successfully"}

def update_post(db: Session, post_id: int, post_update: schemas.PostUpdate, username: str):
    """게시물 수정"""
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user or post.author_id != user.id:
        raise HTTPException(status_code=401, detail="Not authorized to update this post")
    
    post.content = post_update.content
    db.commit()
    db.refresh(post)
    return post

def get_posts_list(db: Session, page: int = 1, limit: int = 10):
    """게시물 목록 조회 (페이지네이션 적용)"""
    # 총 게시물 수 조회
    total = db.query(func.count(models.Post.id)).scalar()
    
    # 페이지네이션 정보 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 게시물 목록 조회
    posts = db.query(models.Post).order_by(
        models.Post.created_at.desc()
    ).offset((page - 1) * limit).limit(limit).all()
    
    return posts, total, page, limit, pages

def get_post_detail(db: Session, post_id: int, username: Optional[str] = None):
    """게시물 상세 정보 조회"""
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(models.post_likes.c.user_id)).filter(
        models.post_likes.c.post_id == post_id
    ).scalar()
    
    # 댓글 수 조회
    comments_count = db.query(func.count(models.Comment.id)).filter(
        models.Comment.post_id == post_id
    ).scalar()
    
    # 현재 사용자가 좋아요 했는지 확인
    is_liked = False
    if username:
        user = user_service.get_user_by_username(db, username)
        if user:
            like = db.query(models.post_likes).filter(
                models.post_likes.c.post_id == post_id,
                models.post_likes.c.user_id == user.id
            ).first()
            is_liked = like is not None
    
    return post, likes_count, comments_count, is_liked

def like_post(db: Session, post_id: int, username: str):
    """게시물 좋아요"""
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 이미 좋아요 했는지 확인
    like = db.query(models.post_likes).filter(
        models.post_likes.c.post_id == post_id,
        models.post_likes.c.user_id == user.id
    ).first()
    
    if like:
        raise HTTPException(status_code=400, detail="Already liked this post")
    
    # 좋아요 추가
    stmt = models.post_likes.insert().values(
        post_id=post_id,
        user_id=user.id
    )
    db.execute(stmt)
    db.commit()
    
    # 좋아요 수 계산
    likes_count = db.query(func.count(models.post_likes.c.user_id)).filter(
        models.post_likes.c.post_id == post_id
    ).scalar()
    
    return {
        "post_id": post_id,
        "is_liked": True,
        "likes_count": likes_count
    }

def unlike_post(db: Session, post_id: int, username: str):
    """게시물 좋아요 취소"""
    post = get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 좋아요 했는지 확인
    like = db.query(models.post_likes).filter(
        models.post_likes.c.post_id == post_id,
        models.post_likes.c.user_id == user.id
    ).first()
    
    if not like:
        raise HTTPException(status_code=400, detail="Haven't liked this post")
    
    # 좋아요 삭제
    stmt = models.post_likes.delete().where(
        models.post_likes.c.post_id == post_id,
        models.post_likes.c.user_id == user.id
    )
    db.execute(stmt)
    db.commit()
    
    # 좋아요 수 계산
    likes_count = db.query(func.count(models.post_likes.c.user_id)).filter(
        models.post_likes.c.post_id == post_id
    ).scalar()
    
    return {
        "post_id": post_id,
        "is_liked": False,
        "likes_count": likes_count
    }