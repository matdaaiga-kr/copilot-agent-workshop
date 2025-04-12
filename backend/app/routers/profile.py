from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database.database import get_db
from ..models.models import User, Post, Follower
from ..security.auth import verify_token

router = APIRouter(tags=["Profile"])

@router.get("", response_model=dict)
def get_profile(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve profile information for the authenticated user
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return {"profile": {"id": user.id, "username": user.username, "profile_image": user.profile_image}}

@router.get("/posts", response_model=dict)
def get_my_posts(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve posts created by the authenticated user
    posts = db.query(Post).filter(Post.owner_id == user_id).all()
    return {"posts": posts}

@router.get("/followers", response_model=dict)
def get_followers(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve followers for the authenticated user
    followers = db.query(Follower).filter(Follower.following_id == user_id).all()
    follower_users = []
    for follow in followers:
        follower = db.query(User).filter(User.id == follow.follower_id).first()
        if follower:
            follower_users.append({
                "id": follower.id,
                "username": follower.username,
                "profile_image": follower.profile_image
            })
    return {"followers": follower_users}

@router.get("/following", response_model=dict)
def get_following(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    # Retrieve users the authenticated user is following
    following = db.query(Follower).filter(Follower.follower_id == user_id).all()
    following_users = []
    for follow in following:
        followed = db.query(User).filter(User.id == follow.following_id).first()
        if followed:
            following_users.append({
                "id": followed.id,
                "username": followed.username,
                "profile_image": followed.profile_image
            })
    return {"following": following_users}