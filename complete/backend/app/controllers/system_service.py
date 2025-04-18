from os import getenv
from dotenv import load_dotenv

# 환경변수 로드
load_dotenv()

def get_health_status():
    """
    시스템 상태 정보를 반환하는 서비스 함수
    """
    return {
        "status": "ok",
        "version": getenv("API_VERSION", "0.1.0")
    }