# Threads-like 애플리케이션 API

이 프로젝트는 Threads와 유사한 소셜 미디어 애플리케이션의 FastAPI 백엔드 API입니다.

## 기능

- 인증 (회원가입, 로그인)
  - JWT 토큰 기반 인증 사용
- 게시글 기능 (작성, 조회, 좋아요, 댓글)
- 프로필 기능 (프로필 조회, 게시글 목록, 팔로워, 팔로잉)

## 기술 스택

- **FastAPI**: 빠른 API 개발을 위한 웹 프레임워크
- **SQLAlchemy**: SQL 데이터베이스 ORM
- **Pydantic**: 데이터 검증 및 설정 관리
- **SQLite**: 데이터베이스
- **Python-jose**: JWT 토큰 처리
- **Passlib**: 패스워드 해싱
- **Uvicorn**: ASGI 서버 구현

## 프로젝트 구조

```
app/
├── controllers/  # 비즈니스 로직
├── core/         # 핵심 기능 (DB, 인증, 설정)
├── models/       # 데이터베이스 모델
├── routers/      # API 라우트
├── schemas/      # Pydantic 스키마
└── main.py       # 애플리케이션 진입점
```

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
SECRET_KEY=your-secret-key
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

## API 문서

- **Swagger UI**: `/docs` 경로에서 접근 가능
- **ReDoc**: `/redoc` 경로에서 접근 가능

## 인증 흐름

1. **회원가입**: `/users/signup` POST 요청을 통해 새 사용자 계정 생성
2. **로그인**: `/users/login` POST 요청을 통해 액세스 토큰 발급
3. **인증 필요 API**: 발급받은 토큰을 요청 헤더의 `Authorization: Bearer {token}` 형태로 포함

## API 엔드포인트

### 사용자

- `POST /users/signup`: 회원가입
- `POST /users/login`: 로그인
- `GET /users/me`: 현재 로그인한 사용자 정보
- `GET /users/{user_id}`: 특정 사용자 정보
- `GET /users/{user_id}/followers`: 해당 사용자의 팔로워 목록
- `GET /users/{user_id}/following`: 해당 사용자가 팔로우하는 사용자 목록

### 게시글

- `GET /posts`: 모든 게시글 목록
- `POST /posts`: 새 게시글 작성
- `GET /posts/{post_id}`: 특정 게시글 조회
- `PUT /posts/{post_id}`: 게시글 수정
- `DELETE /posts/{post_id}`: 게시글 삭제
- `GET /posts/user/{user_id}`: 특정 사용자의 게시글 목록

### 댓글

- `GET /comments/post/{post_id}`: 특정 게시글의 댓글 목록
- `POST /comments`: 댓글 작성
- `PUT /comments/{comment_id}`: 댓글 수정
- `DELETE /comments/{comment_id}`: 댓글 삭제

### 좋아요

- `POST /likes`: 게시글에 좋아요 추가
- `DELETE /likes/{post_id}`: 게시글 좋아요 취소

### 팔로우

- `POST /followers`: 사용자 팔로우
- `DELETE /followers/{following_id}`: 팔로우 취소
