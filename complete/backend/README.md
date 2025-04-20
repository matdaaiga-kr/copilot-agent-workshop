# Threads-like 애플리케이션 백엔드 API

이 프로젝트는 Threads와 유사한 소셜 미디어 애플리케이션의 백엔드 API를 FastAPI로 구현한 것입니다.

## 기능

- 사용자 로그인/등록 (간단한 인증 시스템)
- 게시물 작성, 조회, 수정, 삭제
- 댓글 작성, 조회, 수정, 삭제
- 게시물 좋아요 기능
- 사용자 검색

## 기술 스택

- **FastAPI**: 백엔드 웹 프레임워크
- **SQLAlchemy**: ORM (Object-Relational Mapping)
- **SQLite**: 데이터베이스
- **Pydantic**: 데이터 검증 및 설정 관리
- **Uvicorn**: ASGI 서버

## 프로젝트 구조

```
backend/
├── main.py              # 애플리케이션 진입점
├── requirements.txt     # 패키지 의존성
└── app/
    ├── database.py      # 데이터베이스 설정
    ├── models/          # 데이터베이스 모델
    │   ├── models.py    # SQLAlchemy 모델
    │   └── schemas.py   # Pydantic 스키마
    ├── controllers/     # 비즈니스 로직
    │   ├── auth_service.py
    │   ├── post_service.py
    │   ├── comment_service.py
    │   └── user_service.py
    └── routes/          # API 엔드포인트
        ├── auth.py
        ├── posts.py
        ├── comments.py
        ├── users.py
        ├── search.py
        └── system.py
```

## 실행 방법

### 1. 개발 환경 설정

먼저 필요한 패키지를 설치합니다:

```bash
# 가상 환경 생성 (선택사항)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 또는
venv\Scripts\activate  # Windows

# 필요한 패키지 설치
pip install -r requirements.txt
```

### 2. 환경 변수 설정 (선택사항)

`.env` 파일을 생성하여 다음과 같이 환경 변수를 설정할 수 있습니다:

```
DATABASE_URL=sqlite:///./threads_app.db
API_VERSION=1.0.0
DEBUG=True
```

### 3. 애플리케이션 실행

```bash
# 개발 모드로 실행
python main.py

# 또는 uvicorn을 직접 사용
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

서버는 기본적으로 `http://127.0.0.1:8000`에서 실행됩니다.

## API 문서

FastAPI는 자동으로 API 문서를 생성합니다. 서버를 실행한 후 다음 URL에서 문서를 확인할 수 있습니다:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## API 엔드포인트

### 인증

- `POST /login`: 사용자 로그인

### 사용자

- `GET /users/{userId}`: 사용자 프로필 조회

### 게시물

- `GET /posts`: 게시물 목록 조회
- `POST /posts`: 새 게시물 작성
- `GET /posts/{postId}`: 게시물 상세 정보 조회
- `PUT /posts/{postId}`: 게시물 수정
- `DELETE /posts/{postId}`: 게시물 삭제
- `POST /posts/{postId}/like`: 게시물 좋아요
- `DELETE /posts/{postId}/like`: 게시물 좋아요 취소
- `GET /posts/{postId}/comments`: 게시물 댓글 목록 조회
- `POST /posts/{postId}/comments`: 게시물에 댓글 작성

### 댓글

- `PUT /comments/{commentId}`: 댓글 수정
- `DELETE /comments/{commentId}`: 댓글 삭제

### 검색

- `GET /search`: 사용자 검색

### 시스템

- `GET /`: API 상태 확인

## 프론트엔드 연결

이 백엔드 API는 CORS 설정을 통해 다음 출처에서의 요청을 허용합니다:

- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5173`
- `http://127.0.0.1:5173`

## 라이센스

MIT
