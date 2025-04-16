# Threads-like 애플리케이션 API

## 실행 방법

### 1. 가상 환경 설정

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 2. 의존성 설치

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일에 필요한 환경 변수가 설정되어 있는지 확인하세요:

```
DATABASE_URL=sqlite:///./app.db
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440
```

### 4. 애플리케이션 실행

```bash
# 개발 서버 실행
uvicorn app.main:app --reload

# 또는 Python을 통해 직접 실행
python -m app.main
```
