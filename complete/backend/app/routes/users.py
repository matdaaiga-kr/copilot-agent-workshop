from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from app.models import schemas
from app.controllers import user_service
from app.database import get_db
from typing import List

router = APIRouter(tags=["Users"])

@router.get("/users/{userId}", response_model=schemas.UserProfile)
def get_user_profile(userId: int, db: Session = Depends(get_db)):
    """
    사용자 프로필 조회
    
    - **userId**: 사용자 ID
    """
    user, posts_count = user_service.get_user_profile(db, userId)
    
    # 사용자의 게시물 및 댓글 목록 변환
    user_profile = {
        "id": user.id,
        "username": user.username,
        "profile_image_url": user.profile_image_url,
        "posts_count": posts_count,
        "posts": [],
        "comments": [],
        "created_at": user.created_at,
        "updated_at": user.updated_at
    }
    
    # 사용자 게시물 정보 추가
    for post in user.posts:
        likes_count = len(post.liked_by)
        comments_count = len(post.comments)
        
        post_detail = {
            "id": post.id,
            "content": post.content,
            "author": {
                "id": user.id,
                "username": user.username,
                "profile_image_url": user.profile_image_url
            },
            "likes_count": likes_count,
            "comments_count": comments_count,
            "is_liked": False,  # 기본값
            "created_at": post.created_at,
            "updated_at": post.updated_at
        }
        user_profile["posts"].append(post_detail)
    
    # 사용자 댓글 정보 추가
    for comment in user.comments:
        comment_data = {
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": {
                "id": user.id,
                "username": user.username,
                "profile_image_url": user.profile_image_url
            },
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        }
        user_profile["comments"].append(comment_data)
    
    return user_profile