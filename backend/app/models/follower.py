from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base

class Follower(Base):
    __tablename__ = "followers"
    
    id = Column(Integer, primary_key=True, index=True)
    follower_id = Column(Integer, ForeignKey("users.id"))  # 팔로우하는 사용자
    following_id = Column(Integer, ForeignKey("users.id"))  # 팔로우 당하는 사용자
    
    # 관계 설정
    follower = relationship("User", foreign_keys=[follower_id], back_populates="followings")
    following = relationship("User", foreign_keys=[following_id], back_populates="followers")
    
    # 중복 팔로우 방지를 위한 제약조건
    __table_args__ = (
        UniqueConstraint('follower_id', 'following_id', name='unique_follower_following'),
    )