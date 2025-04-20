from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, system, users, posts, search, comments
from app.database import engine, Base
import uvicorn
import os
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv()

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

# FastAPI 애플리케이션 인스턴스 생성
app = FastAPI(
    title="Threads-like Application API",
    description="This is a Threads-like application backend API that allows users to set a username, post content, follow other users, and interact via comments and likes.",
    version="1.0.0"
)

# CORS 설정
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1",
    "http://127.0.0.1:80",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
    "http://frontend",
    "http://frontend:80",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우트 등록
app.include_router(system.router)
app.include_router(auth.router)
app.include_router(users.router)
app.include_router(search.router)
app.include_router(posts.router)
app.include_router(comments.router)

# 애플리케이션 실행
if __name__ == "__main__":
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)