from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import Dict

from ..models.database import get_db
from ..schemas.schemas import UserCreate, UserLogin, Token, ErrorResponse, SuccessResponse
from ..services.auth import create_access_token, create_refresh_token
from ..services.user import create_user, authenticate_user

router = APIRouter(
    prefix="/auth",
    tags=["인증"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse}
    }
)

security = HTTPBearer()

@router.post("/signup", response_model=SuccessResponse)
async def signup(user: UserCreate, db: Session = Depends(get_db)):
    """
    새로운 사용자 등록
    """
    try:
        db_user = create_user(db, user)
        return {"message": "회원가입이 성공적으로 완료되었습니다"}
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"서버 오류: {str(e)}"
        )

@router.post("/login", response_model=Token)
async def login_for_access_token(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    사용자 인증 및 액세스 토큰 발급
    """
    user = authenticate_user(db, user_data.username, user_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="잘못된 사용자 이름 또는 비밀번호입니다",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 토큰 생성
    access_token = create_access_token(
        data={"sub": user.username, "id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.username, "id": user.id}
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }