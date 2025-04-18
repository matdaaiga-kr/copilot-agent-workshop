from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app.models import models
from app.models.schemas import CommentCreate, CommentUpdate
from app.controllers.user_service import get_or_create_user
from typing import List, Optional, Dict, Any, Tuple
import math
from datetime import datetime

def get_comments_by_post_id(
    db: Session, 
    post_id: int, 
    skip: int = 0, 
    limit: int = 10
) -> Tuple[List[Dict[str, Any]], int, int]:
    """
    특정 게시글의 댓글 목록을 페이지네이션하여 조회
    
    Args:
        db: 데이터베이스 세션
        post_id: 게시글 ID
        skip: 건너뛸 레코드 수
        limit: 가져올 레코드 수
    
    Returns:
        댓글 목록, 전체 댓글 수, 전체 페이지 수
    """
    # 전체 댓글 수 조회
    total = db.query(models.Comment).filter(models.Comment.post_id == post_id).count()
    
    # 페이지 수 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 댓글 목록 조회 (최신순)
    query = db.query(models.Comment).filter(models.Comment.post_id == post_id).order_by(desc(models.Comment.created_at))
    comments = query.offset(skip).limit(limit).all()
    
    # 댓글 정보를 딕셔너리로 변환
    result = []
    for comment in comments:
        result.append({
            "id": comment.id,
            "content": comment.content,
            "post_id": comment.post_id,
            "author": {
                "id": comment.author.id,
                "username": comment.author.username,
                "profile_image_url": comment.author.profile_image_url
            },
            "created_at": comment.created_at,
            "updated_at": comment.updated_at
        })
    
    return result, total, pages

def create_comment(db: Session, post_id: int, comment: CommentCreate) -> Optional[Dict[str, Any]]:
    """
    댓글 생성
    
    Args:
        db: 데이터베이스 세션
        post_id: 게시글 ID
        comment: 댓글 생성 정보
    
    Returns:
        생성된 댓글 정보 또는 None (게시글이 없는 경우)
    """
    # 게시글 확인
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        return None
    
    # 사용자 확인 또는 생성
    user = get_or_create_user(db, comment.username)
    
    # 댓글 생성
    db_comment = models.Comment(
        content=comment.content,
        post_id=post_id,
        author_id=user.id
    )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    
    # 응답 형식으로 변환
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "author": {
            "id": user.id,
            "username": user.username,
            "profile_image_url": user.profile_image_url
        },
        "created_at": db_comment.created_at,
        "updated_at": db_comment.updated_at
    }

def update_comment(
    db: Session, 
    comment_id: int, 
    comment_update: CommentUpdate, 
    username: str
) -> Optional[Dict[str, Any]]:
    """
    댓글 수정
    
    Args:
        db: 데이터베이스 세션
        comment_id: 수정할 댓글 ID
        comment_update: 업데이트할 댓글 내용
        username: 요청한 사용자명 (작성자 확인용)
    
    Returns:
        수정된 댓글 정보 또는 None (권한 없음 또는 댓글이 없는 경우)
    """
    # 댓글 확인
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        return None
    
    # 작성자 확인
    if db_comment.author.username != username:
        return None
    
    # 댓글 수정
    db_comment.content = comment_update.content
    db_comment.updated_at = datetime.now()
    db.commit()
    db.refresh(db_comment)
    
    # 수정된 댓글 정보 반환
    return {
        "id": db_comment.id,
        "content": db_comment.content,
        "post_id": db_comment.post_id,
        "author": {
            "id": db_comment.author.id,
            "username": db_comment.author.username,
            "profile_image_url": db_comment.author.profile_image_url
        },
        "created_at": db_comment.created_at,
        "updated_at": db_comment.updated_at
    }

def delete_comment(db: Session, comment_id: int, username: str) -> bool:
    """
    댓글 삭제
    
    Args:
        db: 데이터베이스 세션
        comment_id: 삭제할 댓글 ID
        username: 요청한 사용자명 (작성자 확인용)
    
    Returns:
        삭제 성공 여부
    """
    # 댓글 확인
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if not db_comment:
        return False
    
    # 작성자 확인
    if db_comment.author.username != username:
        return False
    
    # 댓글 삭제
    db.delete(db_comment)
    db.commit()
    return True