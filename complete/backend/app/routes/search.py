from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UserList
from app.controllers import user_service

# 라우터 생성
router = APIRouter(
    tags=["Search"]
)

@router.get("/search", response_model=UserList)
def search_users(
    username: str = Query(..., description="검색할 사용자명(부분 일치)"),
    page: int = Query(1, description="페이지 번호 (1-indexed)", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    사용자명으로 사용자 검색
    
    - **username**: 검색할 사용자명 (부분 일치)
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 항목 수
    
    사용자명에 입력한 문자열이 포함된 모든 사용자를 검색합니다.
    """
    # 페이지 번호를 0-indexed로 변환
    skip = (page - 1) * limit
    
    # 검색 수행
    users, total, pages = user_service.search_users_by_username(
        db=db, 
        username_query=username,
        skip=skip,
        limit=limit
    )
    
    # 응답 형식으로 변환하여 반환
    return {
        "items": users,
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }