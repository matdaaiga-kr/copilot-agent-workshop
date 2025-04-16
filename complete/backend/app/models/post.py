from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship

from app.core.database import Base

class Post(Base):
    __tablename__ = "posts"
    
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    likes = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    owner_id = Column(Integer, ForeignKey("users.id"))
    
    # 관계 설정
    owner = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    likes_rel = relationship("Like", back_populates="post")