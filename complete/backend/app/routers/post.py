from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.models.user import User
from app.schemas.post import PostCreate, Post as PostSchema, PostUpdate
from app.core.database import get_db
from app.core.auth import get_current_user
from app.controllers import post_controller

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[PostSchema])
def read_posts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """모든 게시글 조회"""
    posts = post_controller.get_posts(db, skip=skip, limit=limit)
    return posts

@router.post("/", response_model=PostSchema)
def create_post(
    post: PostCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """새 게시글 작성"""
    return post_controller.create_post(db=db, post=post, user_id=current_user.id)

@router.get("/{post_id}", response_model=PostSchema)
def read_post(post_id: int, db: Session = Depends(get_db)):
    """ID로 특정 게시글 조회"""
    return post_controller.get_post(db, post_id=post_id)

@router.put("/{post_id}", response_model=PostSchema)
def update_post(
    post_id: int, 
    post: PostUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 수정"""
    return post_controller.update_post(db=db, post_id=post_id, post=post, user_id=current_user.id)

@router.delete("/{post_id}")
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """게시글 삭제"""
    return post_controller.delete_post(db=db, post_id=post_id, user_id=current_user.id)

@router.get("/user/{user_id}", response_model=List[PostSchema])
def read_user_posts(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """특정 사용자의 게시글 조회"""
    posts = post_controller.get_user_posts(db, user_id=user_id, skip=skip, limit=limit)
    return posts