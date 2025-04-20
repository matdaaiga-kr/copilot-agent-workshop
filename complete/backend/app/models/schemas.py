from pydantic import BaseModel, Field, EmailStr, validator, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime

# 기본 응답 스키마
class ErrorResponse(BaseModel):
    error: str
    status_code: int

class SuccessResponse(BaseModel):
    message: str

class HealthCheckResponse(BaseModel):
    status: str = "ok"
    version: str

# 사용자 관련 스키마
class UserLoginSimple(BaseModel):
    username: str = Field(..., description="Username for authentication")

class UserBase(BaseModel):
    id: int
    username: str
    profile_image_url: Optional[str] = None

class UserCreate(BaseModel):
    username: str

class Author(BaseModel):
    id: int
    username: str
    profile_image_url: Optional[str] = None

# 댓글 관련 스키마
class CommentCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=300, description="Text content of the comment")
    username: str = Field(..., description="Username of the comment author (from localStorage)")

class CommentUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=300, description="Updated text content of the comment")

class Comment(BaseModel):
    id: int
    content: str
    post_id: int
    author: Author
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 게시물 관련 스키마
class PostCreate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="Text content of the post")
    username: str = Field(..., description="Username of the post author (from localStorage)")

class PostUpdate(BaseModel):
    content: str = Field(..., min_length=1, max_length=500, description="Updated text content of the post")

class PostDetail(BaseModel):
    id: int
    content: str
    author: Author
    likes_count: int
    comments_count: int
    is_liked: Optional[bool] = False
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 좋아요 관련 스키마
class LikeResponse(BaseModel):
    post_id: int
    is_liked: bool
    likes_count: int

# 페이지네이션 스키마
class PostList(BaseModel):
    items: List[PostDetail]
    total: int
    page: int
    size: int
    pages: int

class CommentList(BaseModel):
    items: List[Comment]
    total: int
    page: int
    size: int
    pages: int

class UserList(BaseModel):
    items: List[UserBase]
    total: int
    page: int
    size: int
    pages: int

# 사용자 프로필 스키마
class UserProfile(BaseModel):
    id: int
    username: str
    profile_image_url: Optional[str] = None
    posts_count: int
    posts: List[PostDetail]
    comments: List[Comment]
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True

# 검증 에러 스키마
class ValidationError(BaseModel):
    loc: List[str]
    msg: str
    type: str

class HTTPValidationError(BaseModel):
    detail: List[ValidationError]