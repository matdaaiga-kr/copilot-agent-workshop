from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.models import User, Follower
from ..models.schemas import UserUpdate, UserResponse
from ..security.auth import verify_token

router = APIRouter(tags=["Users"])

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
def update_my_info(user_update: UserUpdate, db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Update authenticated user's information
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user_update.username:
        user.username = user_update.username
    if user_update.profile_image:
        user.profile_image = user_update.profile_image
        
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