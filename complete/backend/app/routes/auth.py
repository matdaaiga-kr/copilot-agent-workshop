from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import schemas
from app.controllers import auth_service
from app.database import get_db

router = APIRouter(tags=["Login"])

@router.post("/login", response_model=dict, status_code=status.HTTP_200_OK)
def login(user_data: schemas.UserLoginSimple, db: Session = Depends(get_db)):
    """
    사용자 로그인 또는 신규 가입
    
    - **username**: 사용자 이름
    """
    return auth_service.login(db, user_data)