from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from app.core.config import settings
from app.core.database import engine, Base
from app.routers import user, post, comment, like, follower

# 데이터베이스 테이블 생성
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.API_VERSION
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*" "http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)
app.include_router(like.router)
app.include_router(follower.router)

@app.get("/")
def read_root():
    return {
        "message": "Threads-like Application API에 오신 것을 환영합니다!",
        "documentation": "/docs"
    }

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)