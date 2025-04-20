from sqlalchemy.orm import Session
from app.models import models, schemas
from app.controllers import user_service
from typing import Dict

def login(db: Session, user_data: schemas.UserLoginSimple) -> Dict:
    """사용자 로그인 또는 신규 가입"""
    user = user_service.login_user(db, user_data.username)
    return {
        "userId": user.id,
        "username": user.username
    }