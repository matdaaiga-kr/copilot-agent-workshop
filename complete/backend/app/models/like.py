from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship

from app.core.database import Base

class Like(Base):
    __tablename__ = "likes"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    post_id = Column(Integer, ForeignKey("posts.id"))
    
    # 관계 설정
    user = relationship("User", foreign_keys=[user_id], back_populates="likes")
    post = relationship("Post", foreign_keys=[post_id], back_populates="likes_rel")
    
    # 중복 좋아요 방지를 위한 제약조건
    __table_args__ = (
        UniqueConstraint('user_id', 'post_id', name='unique_user_post_like'),
    )