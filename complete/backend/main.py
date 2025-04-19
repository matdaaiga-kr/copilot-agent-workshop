from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import system, posts, auth, comments, users, search
from app.database import engine, Base
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Threads-Like API",
    description="Threads와 유사한 소셜 미디어 애플리케이션을 위한 FastAPI 백엔드",
    version=os.getenv("API_VERSION", "0.1.0")
)

# CORS 미들웨어 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*", "http://localhost:3000", "http://127.0.0.1:3000"],  # 실제 배포 환경에서는 특정 오리진으로 제한해야 함
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(system.router)
app.include_router(auth.router)   # 인증 라우터 추가
app.include_router(users.router)  # 사용자 라우터 추가
app.include_router(search.router)  # 검색 라우터 추가
app.include_router(posts.router)  # 게시글 라우터 추가
app.include_router(comments.router)  # 댓글 라우터 추가

if __name__ == "__main__":
    import uvicorn
    # 디버그 모드 설정
    debug = os.getenv("DEBUG", "False").lower() == "true"
    # 서버 실행
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=debug)