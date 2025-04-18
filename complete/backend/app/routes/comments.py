from fastapi import APIRouter, Depends, HTTPException, status, Path, Header
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

def get_username_from_header(x_username: Optional[str] = Header(None)) -> Optional[str]:
    """
    헤더에서 사용자명을 추출
    (실제 토큰 인증 대신 간단한 사용자명 기반 인증 사용)
    """
    return x_username

@router.put("/{commentId}", response_model=Comment)
def update_comment(
    commentId: int = Path(..., description="수정할 댓글 ID"),
    comment_update: CommentUpdate = ...,
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    댓글을 수정합니다.
    
    - **commentId**: 수정할 댓글 ID
    - **content**: 새 댓글 내용
    
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
    db: Session = Depends(get_db),
    username: Optional[str] = Depends(get_username_from_header)
):
    """
    댓글을 삭제합니다.
    
    - **commentId**: 삭제할 댓글 ID
    
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