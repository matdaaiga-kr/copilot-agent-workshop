from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException, status
from ..models.models import Comment, Post, User
from ..schemas.schemas import CommentCreate, CommentUpdate, PaginationParams
from typing import Optional, Dict, Any

def create_comment(db: Session, post_id: int, comment: CommentCreate, user_id: int):
    """댓글 생성"""
    # 게시물 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    # 댓글 생성
    db_comment = Comment(
        content=comment.content,
        post_id=post_id,
        author_id=user_id
    )
    
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # 작성자 정보 조회
    author = db.query(User).filter(User.id == user_id).first()
    
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "author": {
            "id": author.id,
            "username": author.username,
            "profile_image_url": author.profile_image_url
        },
        "created_at": db_comment.created_at,
        "updated_at": db_comment.updated_at
    }

def get_post_comments(db: Session, post_id: int, pagination: PaginationParams):
    """게시물의 댓글 목록 조회"""
    # 게시물 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    # 총 댓글 수
    total = db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()
    
    # 댓글 목록 조회
    comments = db.query(Comment)\
        .filter(Comment.post_id == post_id)\
        .order_by(desc(Comment.created_at))\
        .offset(pagination.skip)\
        .limit(pagination.limit)\
        .all()
    
    # 댓글 상세 정보
    comments_with_details = []
    for comment in comments:
        author = db.query(User).filter(User.id == comment.author_id).first()
        
        comment_detail = {
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": {
                "id": author.id,
                "username": author.username,
                "profile_image_url": author.profile_image_url
            },
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        }
        
        comments_with_details.append(comment_detail)
    
    # 페이지네이션 정보
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0
    
    return {
        "items": comments_with_details,
        "total": total,
        "page": pagination.page,
        "size": pagination.limit,
        "pages": pages
    }

def update_comment(db: Session, comment_id: int, comment_update: CommentUpdate, user_id: int):
    """댓글 수정"""
    # 댓글 존재 확인
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if db_comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="본인의 댓글만 수정할 수 있습니다"
        )
    
    # 댓글 수정
    db_comment.content = comment_update.content
    db.commit()
    db.refresh(db_comment)
    
    # 작성자 정보 조회
    author = db.query(User).filter(User.id == user_id).first()
    
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "author": {
            "id": author.id,
            "username": author.username,
            "profile_image_url": author.profile_image_url
        },
        "created_at": db_comment.created_at,
        "updated_at": db_comment.updated_at
    }

def delete_comment(db: Session, comment_id: int, user_id: int):
    """댓글 삭제"""
    # 댓글 존재 확인
    db_comment = db.query(Comment).filter(Comment.id == comment_id).first()
    
    if not db_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="댓글을 찾을 수 없습니다"
        )
    
    # 작성자 확인
    if db_comment.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="본인의 댓글만 삭제할 수 있습니다"
        )
    
    # 댓글 삭제
    db.delete(db_comment)
    db.commit()
    
    return {"message": "댓글이 성공적으로 삭제되었습니다"}