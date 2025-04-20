from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from app.models import schemas
from app.controllers import post_service, user_service
from app.database import get_db
from typing import Optional

router = APIRouter(tags=["Posts"])

@router.get("/posts", response_model=schemas.PostList)
def get_posts_list(
    page: int = Query(1, description="페이지 번호", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    게시물 목록 조회
    
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 항목 수
    """
    posts, total, page, limit, pages = post_service.get_posts_list(db, page, limit)
    
    # 응답 구성
    result = {
        "items": [],
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }
    
    # 게시물 정보 변환
    for post in posts:
        # 좋아요 수 계산
        likes_count = len(post.liked_by)
        
        # 댓글 수 계산
        comments_count = len(post.comments)
        
        post_detail = {
            "id": post.id,
            "content": post.content,
            "author": {
                "id": post.author.id,
                "username": post.author.username,
                "profile_image_url": post.author.profile_image_url
            },
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": False,  # 기본값
            "created_at": post.created_at,
            "updated_at": post.updated_at
        }
        result["items"].append(post_detail)
    
    return result

@router.post("/posts", response_model=schemas.PostDetail, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: schemas.PostCreate,
    db: Session = Depends(get_db)
):
    """
    새 게시물 작성
    
    - **content**: 게시물 내용
    - **username**: 작성자 이름 (localStorage에서)
    """
    post = post_service.create_post(db, post_data)
    
    # 게시물 상세 정보 구성
    return {
        "id": post.id,
        "content": post.content,
        "author": {
            "id": post.author.id,
            "username": post.author.username,
            "profile_image_url": post.author.profile_image_url
        },
        "likes_count": 0,
        "comments_count": 0,
        "is_liked": False,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

@router.get("/posts/{postId}", response_model=schemas.PostDetail)
def get_post_detail(
    postId: int,
    username: Optional[str] = Query(None, description="사용자 이름 (선택 사항)"),
    db: Session = Depends(get_db)
):
    """
    게시물 상세 정보 조회
    
    - **postId**: 게시물 ID
    - **username**: 사용자 이름 (선택 사항)
    """
    post, likes_count, comments_count, is_liked = post_service.get_post_detail(db, postId, username)
    
    # 게시물 상세 정보 구성
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

@router.put("/posts/{postId}", response_model=schemas.PostDetail)
def update_post(
    postId: int,
    post_update: schemas.PostUpdate,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    게시물 수정
    
    - **postId**: 수정할 게시물 ID
    - **content**: 수정할 게시물 내용
    - **username**: 작성자 이름
    """
    post = post_service.update_post(db, postId, post_update, username)
    
    # 좋아요 수와 댓글 수 계산
    likes_count = len(post.liked_by)
    comments_count = len(post.comments)
    
    # 현재 사용자의 좋아요 여부 확인
    user = user_service.get_user_by_username(db, username)
    is_liked = user in post.liked_by
    
    # 게시물 상세 정보 구성
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

@router.delete("/posts/{postId}", response_model=schemas.SuccessResponse)
def delete_post(
    postId: int,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    게시물 삭제
    
    - **postId**: 삭제할 게시물 ID
    - **username**: 작성자 이름
    """
    return post_service.delete_post(db, postId, username)

@router.post("/posts/{postId}/like", response_model=schemas.LikeResponse)
def like_post(
    postId: int,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    게시물 좋아요
    
    - **postId**: 좋아요 할 게시물 ID
    - **username**: 사용자 이름
    """
    return post_service.like_post(db, postId, username)

@router.delete("/posts/{postId}/like", response_model=schemas.LikeResponse)
def unlike_post(
    postId: int,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    게시물 좋아요 취소
    
    - **postId**: 좋아요 취소할 게시물 ID
    - **username**: 사용자 이름
    """
    return post_service.unlike_post(db, postId, username)