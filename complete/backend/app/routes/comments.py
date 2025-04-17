from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from ..models.database import get_db
from ..models.models import User
from ..schemas.schemas import CommentCreate, CommentUpdate, Comment, CommentList, SuccessResponse
from ..services.auth import get_current_user
from ..services.comment import update_comment, delete_comment

router = APIRouter(
    prefix="/comments",
    tags=["댓글"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"description": "인증되지 않은 사용자"},
        status.HTTP_404_NOT_FOUND: {"description": "찾을 수 없는 리소스"}
    }
)

@router.put("/{comment_id}", response_model=Comment)
async def update_comment_endpoint(
    comment_id: int,
    comment_update: CommentUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """댓글 수정"""
    return update_comment(db, comment_id, comment_update, current_user.id)

@router.delete("/{comment_id}", response_model=SuccessResponse)
async def delete_comment_endpoint(
    comment_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """댓글 삭제"""
    return delete_comment(db, comment_id, current_user.id)