# Threads-like 애플리케이션 백엔드

FastAPI를 활용한 Threads와 유사한 소셜 미디어 애플리케이션의 백엔드 API입니다.

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **SQLite**: 데이터베이스
- **SQLAlchemy**: ORM(Object-Relational Mapping)
- **Pydantic**: 데이터 유효성 검사
- **Uvicorn**: ASGI 서버

## 요구사항

해당 애플리케이션 실행을 위해 다음 패키지가 필요합니다:

```
fastapi==0.105.0
uvicorn==0.24.0
pydantic==2.4.2
pydantic-settings==2.0.3
sqlalchemy==2.0.23
python-dotenv==1.0.0
aiosqlite==0.19.0
```

## 애플리케이션 실행 방법

### 1. 환경 설정

프로젝트 루트 디렉토리에 `.env` 파일이 있는지 확인합니다. 없다면 다음과 같은 내용으로 생성합니다:

```
DATABASE_URL=sqlite:///./threads_app.db
API_VERSION=0.1.0
DEBUG=True
```

### 2. 필요한 패키지 설치

프로젝트 루트 디렉토리에서 아래 명령어를 실행하여 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

### 3. 애플리케이션 실행

아래 명령어로 애플리케이션을 실행합니다:

```bash
python main.py
```

또는 uvicorn을 직접 사용할 수도 있습니다:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

`--reload` 옵션은 코드 변경 시 서버가 자동으로 재시작되게 합니다. 개발 환경에서만 사용하세요.

### 4. API 문서 확인

애플리케이션이 실행되면 다음 URL에서 자동 생성된 API 문서를 확인할 수 있습니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API 구조

이 애플리케이션은 다음과 같은 주요 엔드포인트를 제공합니다:

- **인증**: 사용자 로그인 및 인증
- **게시글**: 게시글 생성, 조회, 수정, 삭제
- **댓글**: 게시글에 댓글 작성, 수정, 삭제
- **좋아요**: 게시글에 좋아요 추가/제거
- **사용자 검색**: 사용자명으로 검색
- **프로필 조회**: 사용자 프로필 정보 조회

## 프로젝트 구조

```
backend/
│
├── main.py                 # 애플리케이션 진입점
├── requirements.txt        # 의존성 패키지 목록
├── .env                    # 환경 변수 파일
│
├── app/                    # 애플리케이션 패키지
│   ├── database.py         # 데이터베이스 연결 관리
│   │
│   ├── models/             # 데이터 모델 정의
│   │   ├── models.py       # SQLAlchemy 모델
│   │   └── schemas.py      # Pydantic 스키마
│   │
│   ├── controllers/        # 비즈니스 로직 서비스
│   │   ├── auth_service.py
│   │   ├── comment_service.py
│   │   ├── post_service.py
│   │   ├── system_service.py
│   │   └── user_service.py
│   │
│   └── routes/             # API 라우트 정의
│       ├── auth.py
│       ├── comments.py
│       ├── posts.py
│       ├── search.py
│       ├── system.py
│       └── users.py
│
└── json/                   # API 문서화 관련 JSON 파일
```
