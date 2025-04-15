from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from app.schemas.user import User

# 공통 게시글 속성
class PostBase(BaseModel):
    content: str

# 게시글 생성 요청 시 사용
class PostCreate(PostBase):
    pass

# 게시글 수정 요청 시 사용
class PostUpdate(PostBase):
    pass

# 게시글 정보 응답 시 사용
class Post(PostBase):
    id: int
    likes: int
    created_at: datetime
    owner_id: int
    owner: Optional[User] = None
    
    class Config:
        orm_mode = True