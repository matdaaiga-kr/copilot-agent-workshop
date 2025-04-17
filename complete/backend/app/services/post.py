from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from fastapi import HTTPException, status
from ..models.models import Post, User, Like, Comment, Follow
from ..schemas.schemas import PostCreate, PostUpdate, PaginationParams
from typing import Optional, List, Dict, Any

def create_post(db: Session, post: PostCreate, user_id: int):
    """새 게시물 생성"""
    db_post = Post(
        content=post.content,
        author_id=user_id
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    
    # 상세 정보를 포함하여 반환
    return get_post(db, db_post.id, user_id)

def get_post(db: Session, post_id: int, current_user_id: Optional[int] = None):
    """게시물 상세 조회"""
    post = db.query(Post).filter(Post.id == post_id).first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    # 좋아요 수
    likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post_id).scalar()
    
    # 댓글 수
    comments_count = db.query(func.count(Comment.id)).filter(Comment.post_id == post_id).scalar()
    
    # 좋아요 여부 확인
    is_liked = False
    if current_user_id:
        like = db.query(Like).filter(
            Like.user_id == current_user_id,
            Like.post_id == post_id
        ).first()
        is_liked = like is not None
    
    # 작성자 정보
    author = db.query(User).filter(User.id == post.author_id).first()
    
    return {
        "id": post.id,
        "content": post.content,
        "author": {
            "id": author.id,
            "username": author.username,
            "profile_image_url": author.profile_image_url
        },
        "likes_count": likes_count,
        "comments_count": comments_count,
        "is_liked": is_liked,
        "created_at": post.created_at,
        "updated_at": post.updated_at
    }

def update_post(db: Session, post_id: int, post_update: PostUpdate, user_id: int):
    """게시물 수정"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    if db_post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="본인의 게시물만 수정할 수 있습니다"
        )
    
    db_post.content = post_update.content
    db.commit()
    db.refresh(db_post)
    
    return get_post(db, db_post.id, user_id)

def delete_post(db: Session, post_id: int, user_id: int):
    """게시물 삭제"""
    db_post = db.query(Post).filter(Post.id == post_id).first()
    
    if not db_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    if db_post.author_id != user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="본인의 게시물만 삭제할 수 있습니다"
        )
    
    db.delete(db_post)
    db.commit()
    
    return {"message": "게시물이 성공적으로 삭제되었습니다"}

def get_posts_feed(db: Session, user_id: int, pagination: PaginationParams):
    """피드 게시물 목록 (팔로우한 사용자 + 본인 게시물)"""
    # 팔로우한 사용자 ID 목록
    following_ids = [row[0] for row in db.query(Follow.followed_id)
                     .filter(Follow.follower_id == user_id).all()]
    
    # 본인 ID 추가
    author_ids = following_ids + [user_id]
    
    # 총 게시물 수
    total = db.query(func.count(Post.id))\
        .filter(Post.author_id.in_(author_ids)).scalar()
    
    # 게시물 목록 조회
    posts = db.query(Post)\
        .filter(Post.author_id.in_(author_ids))\
        .order_by(desc(Post.created_at))\
        .offset(pagination.skip)\
        .limit(pagination.limit)\
        .all()
    
    # 게시물 상세 정보 추가
    posts_with_details = []
    for post in posts:
        post_detail = get_post(db, post.id, user_id)
        posts_with_details.append(post_detail)
    
    # 페이지네이션 정보
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0
    
    return {
        "items": posts_with_details,
        "total": total,
        "page": pagination.page,
        "size": pagination.limit,
        "pages": pages
    }

def get_user_posts(db: Session, user_id: int, current_user_id: Optional[int], pagination: PaginationParams):
    """특정 사용자의 게시물 목록"""
    # 사용자 존재 확인
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="사용자를 찾을 수 없습니다"
        )
    
    # 총 게시물 수
    total = db.query(func.count(Post.id))\
        .filter(Post.author_id == user_id).scalar()
    
    # 게시물 목록 조회
    posts = db.query(Post)\
        .filter(Post.author_id == user_id)\
        .order_by(desc(Post.created_at))\
        .offset(pagination.skip)\
        .limit(pagination.limit)\
        .all()
    
    # 게시물 상세 정보 추가
    posts_with_details = []
    for post in posts:
        post_detail = get_post(db, post.id, current_user_id)
        posts_with_details.append(post_detail)
    
    # 페이지네이션 정보
    pages = (total + pagination.limit - 1) // pagination.limit if total > 0 else 0
    
    return {
        "items": posts_with_details,
        "total": total,
        "page": pagination.page,
        "size": pagination.limit,
        "pages": pages
    }

def like_post(db: Session, post_id: int, user_id: int):
    """게시물 좋아요"""
    # 게시물 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    # 이미 좋아요했는지 확인
    existing_like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    
    if existing_like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 좋아요한 게시물입니다"
        )
    
    # 좋아요 생성
    new_like = Like(user_id=user_id, post_id=post_id)
    db.add(new_like)
    db.commit()
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post_id).scalar()
    
    return {
        "post_id": post_id,
        "is_liked": True,
        "likes_count": likes_count
    }

def unlike_post(db: Session, post_id: int, user_id: int):
    """게시물 좋아요 취소"""
    # 게시물 존재 확인
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="게시물을 찾을 수 없습니다"
        )
    
    # 좋아요 확인
    like = db.query(Like).filter(
        Like.user_id == user_id,
        Like.post_id == post_id
    ).first()
    
    if not like:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="좋아요하지 않은 게시물입니다"
        )
    
    # 좋아요 삭제
    db.delete(like)
    db.commit()
    
    # 좋아요 수 조회
    likes_count = db.query(func.count(Like.id)).filter(Like.post_id == post_id).scalar()
    
    return {
        "post_id": post_id,
        "is_liked": False,
        "likes_count": likes_count
    }