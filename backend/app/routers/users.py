from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
import shutil
import os
from pathlib import Path
import uuid

from ..database.database import get_db
from ..models.models import User, Follower
from ..models.schemas import UserUpdate, UserResponse
from ..security.auth import verify_token

router = APIRouter(tags=["Users"])

# 이미지를 저장할 디렉토리 설정 - 절대 경로로 변경
BASE_DIR = Path(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
UPLOAD_DIR = BASE_DIR / "uploads" / "profile_images"
# 디렉토리가 없으면 생성
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.get("/me", response_model=dict)
def get_my_info(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve authenticated user's information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"id": user.id, "username": user.username, "profile_image": user.profile_image}}

@router.get("/{id}", response_model=dict)
def get_user_profile(id: int, db: Session = Depends(get_db)):
    # Retrieve specific user's profile
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"user": {"id": user.id, "username": user.username, "profile_image": user.profile_image}}

@router.put("/me", response_model=dict)
def update_my_info(
    db: Session = Depends(get_db),
    user_id: int = Depends(verify_token),
    username: Optional[str] = Form(None),
    profile_image: Optional[UploadFile] = File(None)
):
    # Update authenticated user's information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if username:
        user.username = username
    
    # 프로필 이미지 업로드 처리
    if profile_image and profile_image.filename:
        try:
            # 고유한 파일명 생성 (UUID + 원본 확장자)
            file_extension = os.path.splitext(profile_image.filename)[1]
            unique_filename = f"{uuid.uuid4()}{file_extension}"
            file_path = os.path.join(UPLOAD_DIR, unique_filename)
            
            # 파일 저장
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(profile_image.file, buffer)
            
            # DB에는 상대 경로 저장
            user.profile_image = f"/uploads/profile_images/{unique_filename}"
        except Exception as e:
            # 디버그용 에러 로깅
            print(f"File upload error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"File upload failed: {str(e)}")
        
    db.commit()
    return {"message": "User updated successfully"}

@router.post("/{id}/follow", response_model=dict)
def follow_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Check if the follow relationship already exists
    existing_follow = db.query(Follower).filter(
        Follower.follower_id == user_id, 
        Follower.following_id == id
    ).first()
    
    if existing_follow:
        raise HTTPException(status_code=400, detail="Already following this user")
        
    follow = Follower(follower_id=user_id, following_id=id)
    db.add(follow)
    db.commit()
    return {"message": f"Started following user {id}"}

@router.delete("/{id}/follow", response_model=dict)
def unfollow_user(id: int, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Unfollow a user
    follow = db.query(Follower).filter(
        Follower.follower_id == user_id, 
        Follower.following_id == id
    ).first()
    
    if not follow:
        raise HTTPException(status_code=404, detail="Follow relationship not found")
        
    db.delete(follow)
    db.commit()
    return {"message": f"Stopped following user {id}"}