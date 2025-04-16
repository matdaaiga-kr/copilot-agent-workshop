from pydantic import BaseModel

# 팔로우 요청 시 사용
class FollowerCreate(BaseModel):
    following_id: int

# 팔로워 정보 응답 시 사용
class Follower(BaseModel):
    id: int
    follower_id: int
    following_id: int
    
    class Config:
        orm_mode = True