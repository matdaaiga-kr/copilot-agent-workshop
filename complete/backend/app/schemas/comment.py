from typing import Optional
from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User

# 공통 댓글 속성
class CommentBase(BaseModel):
    content: str

# 댓글 생성 요청 시 사용
class CommentCreate(CommentBase):
    pass

# 댓글 수정 요청 시 사용
class CommentUpdate(CommentBase):
    pass

# 댓글 정보 응답 시 사용
class Comment(CommentBase):
    id: int
    created_at: datetime
    post_id: int
    owner_id: int
    owner: Optional[User] = None
    
    class Config:
        orm_mode = True