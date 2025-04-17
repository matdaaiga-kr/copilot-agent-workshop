from fastapi import FastAPI, HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from jose import JWTError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.routes import router
from app.models.database import engine, Base
from app.schemas.schemas import HealthCheckResponse

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 생성
app = FastAPI(
    title="Threads API",
    description="Threads 애플리케이션을 위한 RESTful API",
    version="1.0.0"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000", "http://127.0.0.1:3000"],  # 실제 배포 환경에서는 구체적인 도메인을 지정하는 것이 좋습니다
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 전역 예외 핸들러
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": str(exc.detail), "status_code": exc.status_code},
    )

@app.exception_handler(JWTError)
async def jwt_error_handler(request: Request, exc: JWTError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={"error": "인증 토큰이 유효하지 않습니다", "status_code": status.HTTP_401_UNAUTHORIZED},
        headers={"WWW-Authenticate": "Bearer"},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": f"서버 오류: {str(exc)}", "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR},
    )

# 헬스 체크 엔드포인트
@app.get("/health", response_model=HealthCheckResponse, tags=["헬스 체크"])
async def health_check():
    """
    API 서버 상태 확인
    """
    return {"status": "ok", "version": "1.0.0"}

# 메인 라우터 등록
app.include_router(router, prefix="/api")

# 애플리케이션 실행
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)