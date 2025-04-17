from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional, List, Any
from datetime import datetime

# 기본 응답 모델
class ErrorResponse(BaseModel):
    error: str
    status_code: int

class SuccessResponse(BaseModel):
    message: str

class HealthCheckResponse(BaseModel):
    status: str = "ok"
    version: str = "1.0.0"

# 유저 스키마
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserLogin(UserBase):
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=30)
    profile_image: Optional[Any] = None

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class UserAuthor(BaseModel):
    id: int
    username: str
    profile_image_url: Optional[str] = None

    class Config:
        orm_mode = True

class UserProfile(UserBase):
    id: int
    profile_image_url: Optional[str] = None
    followers_count: int
    following_count: int
    posts_count: int
    is_following: Optional[bool] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 토큰 스키마
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str
    user_id: int

# 게시물 스키마
class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=500)

class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass

class PostDetail(PostBase):
    id: int
    author: UserAuthor
    likes_count: int
    comments_count: int
    is_liked: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class PostList(BaseModel):
    items: List[PostDetail]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True

# 댓글 스키마
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=300)

class CommentCreate(CommentBase):
    pass

class CommentUpdate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    post_id: int
    author: UserAuthor
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

class CommentList(BaseModel):
    items: List[Comment]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True

# 좋아요 스키마
class LikeResponse(BaseModel):
    post_id: int
    is_liked: bool
    likes_count: int

# 팔로우 스키마
class FollowResponse(BaseModel):
    user_id: int
    is_following: bool

# 유저 목록 스키마
class UserList(BaseModel):
    items: List[UserProfile]
    total: int
    page: int
    size: int
    pages: int

    class Config:
        orm_mode = True

# 페이지네이션 파라미터
class PaginationParams:
    def __init__(self, page: int = 1, limit: int = 10):
        self.page = page
        self.limit = limit
        self.skip = (page - 1) * limit