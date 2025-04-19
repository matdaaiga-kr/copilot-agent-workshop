# Threads-like 애플리케이션 백엔드

이 프로젝트는 Threads와 유사한 소셜 미디어 애플리케이션의 백엔드 API를 제공합니다.

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **SQLAlchemy**: SQL 툴킷 및 ORM
- **SQLite**: 데이터베이스
- **Pydantic**: 데이터 검증 및 설정 관리

## 설치 및 실행 방법

### 1. 가상 환경 설정

먼저, 가상 환경을 생성하고 활성화합니다:

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (맥OS/Linux)
source venv/bin/activate

# 가상 환경 활성화 (Windows)
venv\Scripts\activate
```

### 2. 필요한 패키지 설치

가상 환경이 활성화된 상태에서 필요한 패키지를 설치합니다:

```bash
pip install -r requirements.txt
```

### 3. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가합니다:

```plaintext
DATABASE_URL=sqlite:///./threads_app.db
API_VERSION=0.1.0
DEBUG=True
```

### 4. 애플리케이션 실행

다음 명령어로 애플리케이션을 실행합니다:

```bash
# Python으로 직접 실행
python main.py

# 또는 uvicorn으로 직접 실행
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

애플리케이션이 실행되면 다음 주소로 접속할 수 있습니다:

- API 문서: http://localhost:8000/docs 또는 http://127.0.0.1:8000/docs
- ReDoc 문서: http://localhost:8000/redoc 또는 http://127.0.0.1:8000/redoc

### 5. 가상 환경 비활성화

작업을 마친 후에는 가상 환경을 비활성화할 수 있습니다:

```bash
deactivate
```

## Docker를 사용한 실행 방법

### Docker 실행 (한 번에 처리)

```bash
docker run -d -p 8000:8000 -v $(pwd)/threads_app.db:/app/threads_app.db --name threads-backend devnerdy/threads-backend:latest
```

### 개별 실행 방법 (선택 사항)

이미지만 가져오기:

```bash
docker pull devnerdy/threads-backend:latest
```

볼륨 마운트 없이 실행:

```bash
docker run -d -p 8000:8000 --name threads-backend devnerdy/threads-backend:latest
```

## API 개요

이 API는 다음과 같은 기능을 제공합니다:

- 사용자 로그인 및 프로필 관리
- 게시물 생성, 조회, 수정, 삭제
- 댓글 작성 및 관리
- 게시물 좋아요 기능
- 사용자 검색 기능

## API 엔드포인트

주요 엔드포인트는 다음과 같습니다:

- `/login`: 사용자 로그인
- `/users/{userId}`: 사용자 프로필 조회
- `/search`: 사용자 검색
- `/posts`: 게시물 목록 조회 및 새 게시물 생성
- `/posts/{postId}`: 게시물 상세 조회, 수정, 삭제
- `/posts/{postId}/like`: 게시물 좋아요/좋아요 취소
- `/posts/{postId}/comments`: 게시물 댓글 목록 조회 및 새 댓글 작성
- `/comments/{commentId}`: 댓글 수정 및 삭제
- `/`: 헬스 체크 엔드포인트

## 프론트엔드 연결

이 백엔드 API는 다음 주소에서 실행되는 프론트엔드 애플리케이션과 연결하도록 CORS 설정이 되어 있습니다:

- http://localhost:3000
- http://127.0.0.1:3000

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
