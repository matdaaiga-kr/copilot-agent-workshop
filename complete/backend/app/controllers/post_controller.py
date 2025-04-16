from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List

from app.models.post import Post
from app.models.user import User
from app.schemas.post import PostCreate, PostUpdate

def get_posts(db: Session, skip: int = 0, limit: int = 100):
    """모든 게시글 조회"""
    return db.query(Post).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def get_post(db: Session, post_id: int):
    """ID로 특정 게시글 조회"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시글을 찾을 수 없습니다."
        )
    return post

def get_user_posts(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """특정 사용자의 모든 게시글 조회"""
    return db.query(Post).filter(Post.owner_id == user_id).order_by(Post.created_at.desc()).offset(skip).limit(limit).all()

def create_post(db: Session, post: PostCreate, user_id: int):
    """새 게시글 작성"""
    db_post = Post(
        content=post.content,
        owner_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

def update_post(db: Session, post_id: int, post: PostUpdate, user_id: int):
    """게시글 수정"""
    db_post = get_post(db, post_id)
    
    # 게시글 작성자만 수정 가능
    if db_post.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 게시글을 수정할 권한이 없습니다."
        )
    
    # 게시글 내용 업데이트
    db_post.content = post.content
    
    db.commit()
    db.refresh(db_post)
    return db_post

def delete_post(db: Session, post_id: int, user_id: int):
    """게시글 삭제"""
    db_post = get_post(db, post_id)
    
    # 게시글 작성자만 삭제 가능
    if db_post.owner_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 게시글을 삭제할 권한이 없습니다."
        )
    
    # 게시글 삭제
    db.delete(db_post)
    db.commit()
    
    return {"message": "게시글이 성공적으로 삭제되었습니다."}