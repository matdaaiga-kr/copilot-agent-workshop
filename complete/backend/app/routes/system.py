from fastapi import APIRouter, Depends
from app.controllers.system_service import get_health_status
from app.models.schemas import HealthCheckResponse

# 라우터 생성
router = APIRouter(tags=["System"])

@router.get("/", response_model=HealthCheckResponse)
def root():
    """
    API 헬스 체크 엔드포인트
    시스템 상태 및 API 버전 정보를 반환합니다.
    """
    return get_health_status()