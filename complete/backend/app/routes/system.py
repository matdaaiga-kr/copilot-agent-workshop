import os
from fastapi import APIRouter
from app.models.schemas import HealthCheckResponse

router = APIRouter(tags=["System"])

@router.get("/", response_model=HealthCheckResponse)
def root():
    """
    API 상태 확인 엔드포인트
    """
    # 환경 변수에서 API 버전을 가져옴 (기본값: 1.0.0)
    api_version = os.getenv("API_VERSION", "1.0.0")
    
    return {
        "status": "ok",
        "version": api_version
    }