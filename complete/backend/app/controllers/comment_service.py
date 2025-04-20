from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models import models, schemas
from app.controllers import user_service, post_service
from typing import List, Optional, Dict, Any, Tuple
from fastapi import HTTPException
import math

def get_comment(db: Session, comment_id: int):
    """ID로 댓글 조회"""
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def create_comment(db: Session, post_id: int, comment: schemas.CommentCreate):
    """새 댓글 생성"""
    # 게시물 확인
    post = post_service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 작성자 확인 또는 생성
    user = user_service.get_user_by_username(db, comment.username)
    if not user:
        user_data = schemas.UserCreate(username=comment.username)
        user = user_service.create_user(db, user_data)
    
    # 새 댓글 생성
    db_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        author_id=user.id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def update_comment(db: Session, comment_id: int, comment_update: schemas.CommentUpdate, username: str):
    """댓글 수정"""
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user or comment.author_id != user.id:
        raise HTTPException(status_code=401, detail="Not authorized to update this comment")
    
    comment.content = comment_update.content
    db.commit()
    db.refresh(comment)
    return comment

def delete_comment(db: Session, comment_id: int, username: str):
    """댓글 삭제"""
    comment = get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    
    user = user_service.get_user_by_username(db, username)
    if not user or comment.author_id != user.id:
        raise HTTPException(status_code=401, detail="Not authorized to delete this comment")
    
    db.delete(comment)
    db.commit()
    return {"message": "Comment deleted successfully"}

def get_comments_for_post(db: Session, post_id: int, page: int = 1, limit: int = 10):
    """게시물의 댓글 목록 조회 (페이지네이션 적용)"""
    # 게시물 확인
    post = post_service.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    # 총 댓글 수 조회
    total = db.query(func.count(models.Comment.id)).filter(
        models.Comment.post_id == post_id
    ).scalar()
    
    # 페이지네이션 정보 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 댓글 목록 조회
    comments = db.query(models.Comment).filter(
        models.Comment.post_id == post_id
    ).order_by(models.Comment.created_at.desc()).offset((page - 1) * limit).limit(limit).all()
    
    return comments, total, page, limit, pages