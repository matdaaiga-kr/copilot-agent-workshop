from typing import Optional, List
from pydantic import BaseModel

# 공통 사용자 속성
class UserBase(BaseModel):
    username: str

# 회원가입 요청 시 사용
class UserCreate(UserBase):
    password: str

# 로그인 요청 스키마
class UserLogin(BaseModel):
    username: str
    password: str

# 사용자 정보 응답 시 사용
class User(UserBase):
    id: int
    profile_image: Optional[str] = None
    
    class Config:
        orm_mode = True

# 토큰 응답 스키마
class Token(BaseModel):
    access_token: str
    token_type: str

# 토큰 데이터 스키마
class TokenData(BaseModel):
    user_id: Optional[int] = None