from fastapi import APIRouter, Depends, HTTPException, status, Query, Header
from sqlalchemy.orm import Session
from app.models import schemas
from app.controllers import comment_service
from app.database import get_db

router = APIRouter(tags=["Comments"])

@router.get("/posts/{postId}/comments", response_model=schemas.CommentList)
def get_post_comments(
    postId: int,
    page: int = Query(1, description="페이지 번호", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    게시물의 댓글 목록 조회
    
    - **postId**: 댓글을 조회할 게시물 ID
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 항목 수
    """
    comments, total, page, limit, pages = comment_service.get_comments_for_post(db, postId, page, limit)
    
    # 응답 구성
    result = {
        "items": [],
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }
    
    # 댓글 정보 변환
    for comment in comments:
        comment_data = {
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
        }
        result["items"].append(comment_data)
    
    return result

@router.post("/posts/{postId}/comments", response_model=schemas.Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    postId: int,
    comment_data: schemas.CommentCreate,
    db: Session = Depends(get_db)
):
    """
    게시물에 댓글 작성
    
    - **postId**: 댓글을 작성할 게시물 ID
    - **content**: 댓글 내용
    - **username**: 작성자 이름 (요청 본문에서 제공)
    """
    comment = comment_service.create_comment(db, postId, comment_data)
    
    # 댓글 정보 구성
    return {
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
    }

@router.put("/comments/{commentId}", response_model=schemas.Comment)
def update_comment(
    commentId: int,
    comment_update: schemas.CommentUpdate,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    댓글 수정
    
    - **commentId**: 수정할 댓글 ID
    - **content**: 수정할 댓글 내용
    - **username**: 작성자 이름
    """
    comment = comment_service.update_comment(db, commentId, comment_update, username)
    
    # 댓글 정보 구성
    return {
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
    }

@router.delete("/comments/{commentId}", response_model=schemas.SuccessResponse)
def delete_comment(
    commentId: int,
    username: str = Query(..., description="사용자 이름"),
    db: Session = Depends(get_db)
):
    """
    댓글 삭제
    
    - **commentId**: 삭제할 댓글 ID
    - **username**: 작성자 이름
    """
    return comment_service.delete_comment(db, commentId, username)