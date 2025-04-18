from sqlalchemy.orm import Session
from app.models import models
from app.controllers.user_service import get_or_create_user

def login_user(db: Session, username: str) -> dict:
    """
    사용자명으로 로그인 처리
    존재하는 사용자면 정보를 반환하고, 존재하지 않으면 새로 생성
    
    Args:
        db: 데이터베이스 세션
        username: 로그인하려는 사용자명
    
    Returns:
        사용자 ID와 사용자명이 포함된 사전
    """
    # 사용자 조회 또는 생성
    user = get_or_create_user(db, username)
    
    # 응답 형식으로 변환
    return {
        "userId": user.id,
        "username": user.username
    }