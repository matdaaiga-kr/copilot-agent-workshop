from pydantic import BaseModel

# 좋아요 생성 요청 시 사용
class LikeCreate(BaseModel):
    post_id: int

# 좋아요 정보 응답 시 사용
class Like(BaseModel):
    id: int
    user_id: int
    post_id: int
    
    class Config:
        orm_mode = True