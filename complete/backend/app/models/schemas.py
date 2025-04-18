from pydantic import BaseModel, Field, validator
from typing import Optional, List, Union, Any
from datetime import datetime

class HealthCheckResponse(BaseModel):
    """API 헬스 체크 응답 모델"""
    status: str = Field(description="API 상태", examples=["ok"])
    version: str = Field(description="API 버전")
    
    class Config:
        from_attributes = True

class ValidationError(BaseModel):
    """유효성 검사 오류 정보"""
    loc: List[Union[str, int]] = Field(description="오류 위치")
    msg: str = Field(description="오류 메시지")
    type: str = Field(description="오류 유형")

class HTTPValidationError(BaseModel):
    """HTTP 유효성 검사 오류 응답"""
    detail: List[ValidationError] = Field(description="오류 세부 정보 목록")

class ErrorResponse(BaseModel):
    """표준 오류 응답 형식"""
    error: str = Field(description="오류 메시지")
    status_code: int = Field(description="HTTP 상태 코드")

class SuccessResponse(BaseModel):
    """표준 성공 응답 형식"""
    message: str = Field(description="성공 메시지")

class UserBase(BaseModel):
    """사용자 기본 정보"""
    username: str = Field(description="사용자명")

class UserInfo(BaseModel):
    """간단한 사용자 정보"""
    id: int = Field(description="사용자 ID")
    username: str = Field(description="사용자명")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")

    class Config:
        from_attributes = True

class PostCreate(BaseModel):
    """게시글 생성 모델"""
    content: str = Field(description="게시글 내용", min_length=1, max_length=500)
    username: str = Field(description="게시글 작성자 사용자명")

class PostUpdate(BaseModel):
    """게시글 업데이트 모델"""
    content: str = Field(description="업데이트할 게시글 내용", min_length=1, max_length=500)

class PostDetail(BaseModel):
    """상세 게시글 정보"""
    id: int = Field(description="게시글 ID")
    content: str = Field(description="게시글 내용")
    author: UserInfo = Field(description="작성자 정보")
    likes_count: int = Field(description="좋아요 수")
    comments_count: int = Field(description="댓글 수")
    is_liked: Optional[bool] = Field(False, description="인증된 사용자가 좋아요 했는지 여부")
    created_at: datetime = Field(description="작성 일시")
    updated_at: Optional[datetime] = Field(None, description="수정 일시")

    class Config:
        from_attributes = True

class PostList(BaseModel):
    """게시글 목록 (페이지네이션)"""
    items: List[PostDetail] = Field(description="게시글 목록")
    total: int = Field(description="전체 게시글 수")
    page: int = Field(description="현재 페이지 번호")
    size: int = Field(description="페이지 당 항목 수")
    pages: int = Field(description="전체 페이지 수")

class CommentCreate(BaseModel):
    """댓글 생성 모델"""
    content: str = Field(description="댓글 내용", min_length=1, max_length=300)
    username: str = Field(description="댓글 작성자 사용자명")

class CommentUpdate(BaseModel):
    """댓글 업데이트 모델"""
    content: str = Field(description="업데이트할 댓글 내용", min_length=1, max_length=300)

class Comment(BaseModel):
    """댓글 정보"""
    id: int = Field(description="댓글 ID")
    content: str = Field(description="댓글 내용")
    post_id: int = Field(description="게시글 ID")
    author: UserInfo = Field(description="작성자 정보")
    created_at: datetime = Field(description="작성 일시")
    updated_at: Optional[datetime] = Field(None, description="수정 일시")

    class Config:
        from_attributes = True

class CommentList(BaseModel):
    """댓글 목록 (페이지네이션)"""
    items: List[Comment] = Field(description="댓글 목록")
    total: int = Field(description="전체 댓글 수")
    page: int = Field(description="현재 페이지 번호")
    size: int = Field(description="페이지 당 항목 수")
    pages: int = Field(description="전체 페이지 수")

class LikeResponse(BaseModel):
    """좋아요/좋아요 취소 응답"""
    post_id: int = Field(description="게시글 ID")
    is_liked: bool = Field(description="사용자가 게시글을 좋아요 했는지 여부")
    likes_count: int = Field(description="게시글의 업데이트된 좋아요 수")

    class Config:
        from_attributes = True

class UserLoginSimple(BaseModel):
    """
    간단한 사용자 로그인 자격 증명
    사용자명만으로 인증 처리
    """
    username: str = Field(description="인증에 사용되는 사용자명")
    
    class Config:
        from_attributes = True

class UserLoginResponse(BaseModel):
    """
    로그인 성공 시 응답 모델
    """
    userId: int = Field(description="사용자 ID")
    username: str = Field(description="세션에 설정된 사용자명")
    
    class Config:
        from_attributes = True

class UserProfile(BaseModel):
    """사용자 프로필 정보"""
    id: int = Field(description="사용자 ID")
    username: str = Field(description="사용자명")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")
    posts_count: int = Field(description="게시글 수")
    posts: List[PostDetail] = Field(description="사용자의 게시글 목록")
    comments: List[Comment] = Field(description="사용자의 댓글 목록")
    created_at: datetime = Field(description="계정 생성 일시")
    updated_at: Optional[datetime] = Field(None, description="프로필 수정 일시")
    
    class Config:
        from_attributes = True

class UserListItem(BaseModel):
    """검색 결과에 표시되는 간단한 사용자 정보"""
    id: int = Field(description="사용자 ID")
    username: str = Field(description="사용자명")
    profile_image_url: Optional[str] = Field(None, description="프로필 이미지 URL")
    
    class Config:
        from_attributes = True

class UserList(BaseModel):
    """사용자 목록 (페이지네이션)"""
    items: List[UserListItem] = Field(description="사용자 목록")
    total: int = Field(description="전체 검색 결과 수")
    page: int = Field(description="현재 페이지 번호")
    size: int = Field(description="페이지 당 항목 수")
    pages: int = Field(description="전체 페이지 수")
    
    class Config:
        from_attributes = True