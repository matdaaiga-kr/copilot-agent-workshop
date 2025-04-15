from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.follower import Follower
from app.models.user import User
from app.schemas.follower import FollowerCreate

def follow_user(db: Session, follower: FollowerCreate, current_user_id: int):
    """다른 사용자 팔로우하기"""
    # 자기 자신을 팔로우하는지 확인
    if follower.following_id == current_user_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="자기 자신을 팔로우할 수 없습니다."
        )
    
    # 팔로우할 사용자가 존재하는지 확인
    following_user = db.query(User).filter(User.id == follower.following_id).first()
    if not following_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="해당 사용자를 찾을 수 없습니다."
        )
    
    # 이미 팔로우하고 있는지 확인
    existing_follow = db.query(Follower).filter(
        Follower.follower_id == current_user_id,
        Follower.following_id == follower.following_id
    ).first()
    
    if existing_follow:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 팔로우한 사용자입니다."
        )
    
    # 새 팔로우 관계 생성
    db_follower = Follower(
        follower_id=current_user_id,
        following_id=follower.following_id
    )
    
    db.add(db_follower)
    db.commit()
    db.refresh(db_follower)
    
    return db_follower

def unfollow_user(db: Session, following_id: int, current_user_id: int):
    """팔로우 취소하기"""
    # 팔로우 관계 확인
    follow_relation = db.query(Follower).filter(
        Follower.follower_id == current_user_id,
        Follower.following_id == following_id
    ).first()
    
    if not follow_relation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="팔로우 관계가 없습니다."
        )
    
    # 팔로우 관계 삭제
    db.delete(follow_relation)
    db.commit()
    
    return {"message": "언팔로우 되었습니다."}