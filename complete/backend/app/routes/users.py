from fastapi import APIRouter, Depends, HTTPException, status, Path
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UserProfile, ErrorResponse
from app.controllers import user_service

# 라우터 생성
router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

@router.get("/{userId}", response_model=UserProfile)
def get_user_profile(
    userId: int = Path(..., description="조회할 사용자 ID"),
    db: Session = Depends(get_db)
):
    """
    특정 사용자의 프로필 정보를 조회합니다.
    
    - **userId**: 조회할 사용자 ID
    
    프로필 정보에는 사용자의 기본 정보, 게시글 목록, 댓글 목록 등이 포함됩니다.
    """
    profile = user_service.get_user_profile(db, userId)
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={"error": "사용자를 찾을 수 없습니다.", "status_code": 404}
        )
    
    return profile