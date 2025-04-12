from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta

from ..database.database import get_db
from ..models.models import User
from ..models.schemas import UserCreate, UserLogin, Token
from ..security.auth import get_password_hash, verify_password, create_access_token, create_refresh_token

router = APIRouter(tags=["Authentication"])

@router.post("/signup", response_model=dict)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = db.query(User).filter(User.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash password and save user
    hashed_password = get_password_hash(user.password)
    new_user = User(username=user.username, hashed_password=hashed_password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "User created successfully"}

@router.post("/login", response_model=Token)
def login(user: UserLogin, db: Session = Depends(get_db)):
    # Retrieve user from database
    existing_user = db.query(User).filter(User.username == user.username).first()
    
    # 사용자가 존재하지 않거나 비밀번호가 일치하지 않을 경우
    if not existing_user:
        raise HTTPException(status_code=401, detail="사용자가 존재하지 않습니다")

    # Generate tokens
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": str(existing_user.id)}, expires_delta=access_token_expires
    )
    refresh_token = create_refresh_token(data={"sub": str(existing_user.id)})

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}