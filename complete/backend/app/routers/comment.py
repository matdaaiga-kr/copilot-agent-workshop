from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.schemas.comment import CommentCreate, Comment as CommentSchema, CommentUpdate
from app.core.database import get_db
from app.core.auth import get_current_user
from app.controllers import comment_controller

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{post_id}", response_model=List[CommentSchema])
def read_comments_by_post(
    post_id: int, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db)
):
    """게시물의 댓글 조회"""
    comments = comment_controller.get_comments_by_post(db, post_id=post_id, skip=skip, limit=limit)
    return comments

@router.post("/{post_id}", response_model=CommentSchema)
def create_comment(
    post_id: int,
    comment: CommentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글 작성"""
    # 요청 바디의 post_id 대신 URL 경로의 post_id 사용
    return comment_controller.create_comment(db=db, comment=comment, post_id=post_id, user_id=current_user.id)

@router.put("/{post_id}/{comment_id}", response_model=CommentSchema)
def update_comment(
    post_id: int,
    comment_id: int, 
    comment: CommentUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글 수정"""
    return comment_controller.update_comment(
        db=db, 
        comment_id=comment_id, 
        comment=comment, 
        user_id=current_user.id, 
        post_id=post_id
    )

@router.delete("/{post_id}/{comment_id}")
def delete_comment(
    post_id: int,
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """댓글 삭제"""
    return comment_controller.delete_comment(
        db=db, 
        comment_id=comment_id, 
        user_id=current_user.id,
        post_id=post_id
    )