from fastapi import APIRouter, Depends, HTTPException, status, Path, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import CommentUpdate, Comment, SuccessResponse, ErrorResponse
from app.controllers import comment_service

# 라우터 생성
router = APIRouter(
    prefix="/comments",
    tags=["Comments"]
)

@router.put("/{commentId}", response_model=Comment)
def update_comment(
    commentId: int = Path(..., description="수정할 댓글 ID"),
    comment_update: CommentUpdate = ...,
    username: str = Query(..., description="작성자 사용자명"),
    db: Session = Depends(get_db)
):
    """
    댓글을 수정합니다.
    
    - **commentId**: 수정할 댓글 ID
    - **content**: 새 댓글 내용
    - **username**: 작성자 사용자명 (쿼리 파라미터)
    
    인증된 사용자만 자신이 작성한 댓글을 수정할 수 있습니다.
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    updated_comment = comment_service.update_comment(db, commentId, comment_update, username)
    if not updated_comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "댓글을 찾을 수 없거나 수정 권한이 없습니다.", "status_code": 404}
        )
    
    return updated_comment

@router.delete("/{commentId}", response_model=SuccessResponse)
def delete_comment(
    commentId: int = Path(..., description="삭제할 댓글 ID"),
    username: str = Query(..., description="작성자 사용자명"),
    db: Session = Depends(get_db)
):
    """
    댓글을 삭제합니다.
    
    - **commentId**: 삭제할 댓글 ID
    - **username**: 작성자 사용자명 (쿼리 파라미터)
    
    인증된 사용자만 자신이 작성한 댓글을 삭제할 수 있습니다.
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"error": "인증이 필요합니다.", "status_code": 401}
        )
    
    success = comment_service.delete_comment(db, commentId, username)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "댓글을 찾을 수 없거나 삭제 권한이 없습니다.", "status_code": 404}
        )
    
    return {"message": "댓글이 성공적으로 삭제되었습니다."}