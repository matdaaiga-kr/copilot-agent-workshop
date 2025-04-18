from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.schemas import UserLoginSimple, UserLoginResponse
from app.controllers import auth_service

# 라우터 생성
router = APIRouter(
    tags=["Login"]
)

@router.post("/login", response_model=UserLoginResponse)
def login(
    login_data: UserLoginSimple,
    db: Session = Depends(get_db)
):
    """
    사용자명으로 로그인 처리
    
    - **username**: 인증에 사용할 사용자명
    
    존재하는 사용자명이면 해당 사용자 정보를 반환하고,
    존재하지 않는 사용자명이면 새로운 사용자를 생성함
    """
    # 사용자명 검증
    if not login_data.username or len(login_data.username.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": "유효한 사용자명을 입력해주세요", "status_code": 400}
        )
    
    # 로그인 처리
    result = auth_service.login_user(db, login_data.username.strip())
    
    return result