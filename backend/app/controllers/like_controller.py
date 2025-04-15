from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.like import Like
from app.models.post import Post
from app.schemas.like import LikeCreate

def get_post_likes(db: Session, post_id: int):
    """게시물의 모든 좋아요 조회"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    # 해당 게시글의 모든 좋아요 반환
    likes = db.query(Like).filter(Like.post_id == post_id).all()
    return likes

def like_post(db: Session, like: LikeCreate, user_id: int):
    """게시글에 좋아요 추가"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == like.post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    # 이미 좋아요한 게시글인지 확인
    existing_like = db.query(Like).filter(
        Like.post_id == like.post_id,
        Like.user_id == user_id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 좋아요한 게시글입니다."
        )
    
    # 새 좋아요 생성
    db_like = Like(
        user_id=user_id,
        post_id=like.post_id
    )
    
    # 게시글의 좋아요 수 증가
    post.likes += 1
    
    db.add(db_like)
    db.commit()
    db.refresh(db_like)
    db.refresh(post)
    
    return db_like

def unlike_post(db: Session, post_id: int, user_id: int):
    """게시글 좋아요 취소"""
    # 게시글 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    
    # 좋아요 기록 확인 (사용자와 게시물 ID로)
    like = db.query(Like).filter(
        Like.post_id == post_id,
        Like.user_id == user_id
    ).first()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="좋아요 기록이 없거나 권한이 없습니다."
        )
    
    # 좋아요 삭제
    db.delete(like)
    
    # 게시글의 좋아요 수 감소
    if post.likes > 0:
        post.likes -= 1
    
    db.commit()
    db.refresh(post)
    
    return {"message": "좋아요가 취소되었습니다."}