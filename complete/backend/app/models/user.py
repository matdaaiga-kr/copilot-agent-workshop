from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    profile_image = Column(String, nullable=True)
    
    # 관계 설정
    posts = relationship("Post", back_populates="owner")
    comments = relationship("Comment", back_populates="owner")
    likes = relationship("Like", foreign_keys="Like.user_id", back_populates="user")
    followers = relationship("Follower", foreign_keys="Follower.following_id", back_populates="following")
    followings = relationship("Follower", foreign_keys="Follower.follower_id", back_populates="follower")