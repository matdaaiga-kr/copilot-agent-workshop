from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# 환경 변수에서 데이터베이스 URL 가져오기
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./threads_app.db")

# SQLAlchemy 엔진 생성
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# 세션 팩토리 생성
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base 클래스 생성 - 모든 모델이 이를 상속받을 예정
Base = declarative_base()

# 데이터베이스 세션 Dependency
def get_db():
    """
    FastAPI 라우트에서 사용할 데이터베이스 세션 의존성(Dependency)
    요청마다 새로운 DB 세션을 생성하고 요청 완료 후 세션을 닫음
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()