from fastapi import APIRouter, Depends, HTTPException, status, Query, Path, Header
from typing import Optional, List
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import (
    PostCreate, PostUpdate, PostDetail, PostList, 
    CommentCreate, Comment, CommentList, 
    LikeResponse, SuccessResponse, ErrorResponse
)
from app.controllers import post_service, comment_service

# 라우터 생성
router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

def get_username_from_header(x_username: Optional[str] = Header(None)) -> Optional[str]:
    """
    헤더에서 사용자명을 추출
    (실제 토큰 인증 대신 간단한 사용자명 기반 인증 사용)
    """
    return x_username

@router.get("", response_model=PostList)
def get_posts_list(
    page: int = Query(1, description="페이지 번호 (1-indexed)", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    게시글 목록을 가져옵니다.
    
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 게시글 수
    """
    skip = (page - 1) * limit
    posts, total, pages = post_service.get_posts(db, skip=skip, limit=limit, current_username=username)
    
    return {
        "items": posts,
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }

@router.post("", response_model=PostDetail, status_code=status.HTTP_201_CREATED)
def create_post(
    post: PostCreate,
    db: Session = Depends(get_db)
):
    """
    새 게시글을 생성합니다.
    
    - **content**: 게시글 내용
    - **username**: 작성자 사용자명
    """
    return post_service.create_post(db, post)

@router.get("/{postId}", response_model=PostDetail)
def get_post_detail(
    postId: int = Path(..., description="조회할 게시글 ID"),
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    특정 게시글의 상세 정보를 가져옵니다.
    
    - **postId**: 조회할 게시글 ID
    """
    post = post_service.get_post(db, post_id=postId, current_username=username)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없습니다.", "status_code": 404}
        )
    return post

@router.put("/{postId}", response_model=PostDetail)
def update_post(
    postId: int = Path(..., description="수정할 게시글 ID"),
    post_update: PostUpdate = ...,
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    게시글을 수정합니다.
    
    - **postId**: 수정할 게시글 ID
    - **content**: 새 게시글 내용
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    updated_post = post_service.update_post(db, postId, post_update, username)
    if not updated_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없거나 수정 권한이 없습니다.", "status_code": 404}
        )
    return updated_post

@router.delete("/{postId}", response_model=SuccessResponse)
def delete_post(
    postId: int = Path(..., description="삭제할 게시글 ID"),
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    게시글을 삭제합니다.
    
    - **postId**: 삭제할 게시글 ID
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    success = post_service.delete_post(db, postId, username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없거나 삭제 권한이 없습니다.", "status_code": 404}
        )
    
    return {"message": "게시글이 성공적으로 삭제되었습니다."}

@router.post("/{postId}/like", response_model=LikeResponse)
def like_post(
    postId: int = Path(..., description="좋아요할 게시글 ID"),
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    게시글에 좋아요를 추가합니다.
    
    - **postId**: 좋아요할 게시글 ID
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    like_result = post_service.like_post(db, postId, username)
    if not like_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없습니다.", "status_code": 404}
        )
    
    return like_result

@router.delete("/{postId}/like", response_model=LikeResponse)
def unlike_post(
    postId: int = Path(..., description="좋아요 취소할 게시글 ID"),
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    게시글의 좋아요를 취소합니다.
    
    - **postId**: 좋아요 취소할 게시글 ID
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    unlike_result = post_service.unlike_post(db, postId, username)
    if not unlike_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없습니다.", "status_code": 404}
        )
    
    return unlike_result

@router.get("/{postId}/comments", response_model=CommentList)
def get_post_comments(
    postId: int = Path(..., description="댓글을 조회할 게시글 ID"),
    page: int = Query(1, description="페이지 번호 (1-indexed)", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    특정 게시글의 댓글 목록을 가져옵니다.
    
    - **postId**: 댓글을 조회할 게시글 ID
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 댓글 수
    """
    # 게시글 존재 여부 확인
    post = post_service.get_post(db, post_id=postId)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없습니다.", "status_code": 404}
        )
    
    skip = (page - 1) * limit
    comments, total, pages = comment_service.get_comments_by_post_id(
        db, post_id=postId, skip=skip, limit=limit
    )
    
    return {
        "items": comments,
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }

@router.post("/{postId}/comments", response_model=Comment, status_code=status.HTTP_201_CREATED)
def create_comment(
    postId: int = Path(..., description="댓글을 작성할 게시글 ID"),
    comment: CommentCreate = ...,
    db: Session = Depends(get_db)
):
    """
    게시글에 새 댓글을 작성합니다.
    
    - **postId**: 댓글을 작성할 게시글 ID
    - **content**: 댓글 내용
    - **username**: 작성자 사용자명
    """
    result = comment_service.create_comment(db, postId, comment)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "게시글을 찾을 수 없습니다.", "status_code": 404}
        )
    
    return result