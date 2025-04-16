from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.follower import FollowerCreate, Follower as FollowerSchema
from app.core.database import get_db
from app.core.auth import get_current_user
from app.controllers import follower_controller

router = APIRouter(
    prefix="/follows",
    tags=["followers"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=FollowerSchema)
def follow_user(
    follower: FollowerCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """사용자 팔로우하기"""
    return follower_controller.follow_user(db=db, follower=follower, current_user_id=current_user.id)

@router.delete("/", status_code=status.HTTP_200_OK)
def unfollow_user(
    follower: FollowerCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """팔로우 취소하기"""
    return follower_controller.unfollow_user(db=db, following_id=follower.following_id, current_user_id=current_user.id)