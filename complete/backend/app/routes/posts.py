from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models.database import get_db
from ..models.models import User
from ..schemas.schemas import (
    PostCreate, PostDetail, PostUpdate, PostList, 
    LikeResponse, SuccessResponse, PaginationParams,
    CommentCreate, CommentUpdate, Comment, CommentList
)
from ..services.auth import get_current_user
from ..services.post import create_post, get_post, update_post, delete_post, get_posts_feed, get_user_posts, like_post, unlike_post
from ..services.comment import create_comment, get_post_comments, update_comment, delete_comment

router = APIRouter(
    prefix="/posts",
    tags=["게시물"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "인증되지 않은 사용자"},
        status.HTTP_404_NOT_FOUND: {"description": "찾을 수 없는 리소스"}
    }
)

@router.post("/", response_model=PostDetail)
async def create_new_post(
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """새 게시물 작성"""
    return create_post(db, post, current_user.id)

@router.get("/", response_model=PostList)
async def read_posts_feed(
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=50, description="페이지당 항목 수"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """피드 게시물 목록 (팔로우한 사용자 + 본인 게시물)"""
    pagination = PaginationParams(page=page, limit=limit)
    return get_posts_feed(db, current_user.id, pagination)

@router.get("/user/{user_id}", response_model=PostList)
async def read_user_posts(
    user_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=50, description="페이지당 항목 수"),
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """특정 사용자의 게시물 목록"""
    pagination = PaginationParams(page=page, limit=limit)
    current_user_id = current_user.id if current_user else None
    return get_user_posts(db, user_id, current_user_id, pagination)

@router.get("/{post_id}", response_model=PostDetail)
async def read_post(
    post_id: int,
    current_user: Optional[User] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물 상세 조회"""
    current_user_id = current_user.id if current_user else None
    return get_post(db, post_id, current_user_id)

@router.put("/{post_id}", response_model=PostDetail)
async def update_post_endpoint(
    post_id: int,
    post_update: PostUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물 수정"""
    return update_post(db, post_id, post_update, current_user.id)

@router.delete("/{post_id}", response_model=SuccessResponse)
async def delete_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물 삭제"""
    return delete_post(db, post_id, current_user.id)

@router.post("/{post_id}/like", response_model=LikeResponse)
async def like_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물 좋아요"""
    return like_post(db, post_id, current_user.id)

@router.delete("/{post_id}/like", response_model=LikeResponse)
async def unlike_post_endpoint(
    post_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물 좋아요 취소"""
    return unlike_post(db, post_id, current_user.id)

@router.post("/{post_id}/comments", response_model=Comment)
async def create_comment_for_post(
    post_id: int,
    comment: CommentCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """게시물에 새 댓글 작성"""
    return create_comment(db, post_id, comment, current_user.id)

@router.get("/{post_id}/comments", response_model=CommentList)
async def read_comments_for_post(
    post_id: int,
    page: int = Query(1, ge=1, description="페이지 번호"),
    limit: int = Query(10, ge=1, le=100, description="페이지당 항목 수"),
    db: Session = Depends(get_db)
):
    """게시물의 댓글 목록 조회"""
    pagination = PaginationParams(page=page, limit=limit)
    return get_post_comments(db, post_id, pagination)