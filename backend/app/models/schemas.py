from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class UserUpdate(BaseModel):
    username: Optional[str] = None
    profile_image: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    profile_image: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    content: str

class PostUpdate(BaseModel):
    content: str

class PostResponse(BaseModel):
    id: int
    content: str
    owner_id: int
    likes: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentUpdate(BaseModel):
    content: str

class CommentResponse(BaseModel):
    id: int
    content: str
    post_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str