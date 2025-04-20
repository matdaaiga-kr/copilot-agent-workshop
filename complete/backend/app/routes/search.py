from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.models import schemas
from app.controllers import user_service
from app.database import get_db
import math

router = APIRouter(tags=["Search"])

@router.get("/search", response_model=schemas.UserList)
def search_users(
    username: str = Query(..., description="검색할 사용자 이름"),
    page: int = Query(1, description="페이지 번호", ge=1),
    limit: int = Query(10, description="페이지당 항목 수", ge=1, le=100),
    db: Session = Depends(get_db)
):
    """
    사용자 이름으로 검색
    
    - **username**: 검색할 사용자 이름 (부분 일치)
    - **page**: 페이지 번호 (1부터 시작)
    - **limit**: 페이지당 항목 수
    """
    users, total = user_service.search_users(db, username, page, limit)
    
    # 총 페이지 수 계산
    pages = math.ceil(total / limit) if total > 0 else 0
    
    # 응답 구성
    result = {
        "items": [],
        "total": total,
        "page": page,
        "size": limit,
        "pages": pages
    }
    
    # 검색 결과 사용자 정보 변환
    for user in users:
        user_data = {
            "id": user.id,
            "username": user.username,
            "profile_image_url": user.profile_image_url
        }
        result["items"].append(user_data)
    
    return result