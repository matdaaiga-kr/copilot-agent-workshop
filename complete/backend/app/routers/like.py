from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.schemas.like import LikeCreate, Like as LikeSchema
from app.core.database import get_db
from app.core.auth import get_current_user
from app.controllers import like_controller

router = APIRouter(
    prefix="/likes",
    tags=["likes"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{post_id}", response_model=List[LikeSchema])
def get_post_likes(
    post_id: int,
    db: Session = Depends(get_db)
):
    """게시물의 좋아요 조회"""
    return like_controller.get_post_likes(db=db, post_id=post_id)

@router.post("/{post_id}", response_model=LikeSchema)
def like_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글에 좋아요 추가"""
    like = LikeCreate(post_id=post_id)
    return like_controller.like_post(db=db, like=like, user_id=current_user.id)

@router.delete("/{post_id}")
def unlike_post(
    post_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 좋아요 취소"""
    return like_controller.unlike_post(db=db, post_id=post_id, user_id=current_user.id)