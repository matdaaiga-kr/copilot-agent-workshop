# Threads-like 애플리케이션 백엔드

FastAPI 기반의 Threads-like 소셜 미디어 애플리케이션 백엔드입니다. 이 백엔드는 사용자 인증, 게시물, 댓글, 좋아요, 팔로우 기능을 지원합니다.

## 기능

- **인증**: 회원가입, 로그인 (JWT 토큰 기반)
- **게시물**: 게시물 작성, 조회, 수정, 삭제, 좋아요
- **댓글**: 댓글 작성, 조회, 수정, 삭제
- **프로필**: 사용자 프로필 조회, 팔로우/언팔로우
- **피드**: 팔로우한 사용자와 본인의 게시물 타임라인 제공

## 기술 스택

- **FastAPI**: 고성능 웹 프레임워크
- **SQLite**: 데이터베이스
- **SQLAlchemy**: ORM(Object-Relational Mapping)
- **PyJWT**: JWT 토큰 인증
- **Pydantic**: 데이터 검증 및 설정 관리

## 시작하기

### 필수 조건

- Python 3.8 이상
- pip (파이썬 패키지 관리자)

### 설치

1. 저장소 클론

```bash
git clone <repository-url>
cd backend
```

2. 가상 환경 생성 및 활성화

```bash
# 가상 환경 생성
python -m venv venv

# 가상 환경 활성화 (Windows)
venv\Scripts\activate

# 가상 환경 활성화 (macOS/Linux)
source venv/bin/activate
```

3. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

4. 환경 변수 설정

`.env` 파일을 생성하고 다음 내용을 추가:

```
# JWT 설정
SECRET_KEY=09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# 데이터베이스 설정
DATABASE_URL=sqlite:///./threads_app.db
```

> 참고: 실제 배포 환경에서는 `.env` 파일을 버전 관리에 포함시키지 말고, 더 복잡한 보안 키를 사용하세요.

### 실행

```bash
uvicorn main:app --reload
```

서버는 기본적으로 `http://localhost:8000`에서 실행됩니다.

### API 문서

FastAPI는 자동으로 API 문서를 생성합니다:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 프로젝트 구조

```
backend/
│
├── app/
│   ├── models/           # 데이터베이스 모델
│   │   ├── database.py   # 데이터베이스 연결 설정
│   │   └── models.py     # SQLAlchemy 모델 정의
│   │
│   ├── routes/           # API 라우트
│   │   ├── __init__.py   # 라우트 초기화
│   │   ├── auth.py       # 인증 관련 엔드포인트
│   │   ├── comments.py   # 댓글 관련 엔드포인트
│   │   ├── posts.py      # 게시물 관련 엔드포인트
│   │   ├── profile.py    # 프로필 관련 엔드포인트
│   │   └── users.py      # 사용자 관련 엔드포인트
│   │
│   ├── schemas/          # Pydantic 모델(스키마)
│   │   └── schemas.py    # 데이터 검증 및 직렬화 스키마
│   │
│   └── services/         # 비즈니스 로직
│       ├── auth.py       # 인증 관련 서비스
│       ├── comment.py    # 댓글 관련 서비스
│       ├── post.py       # 게시물 관련 서비스
│       └── user.py       # 사용자 관련 서비스
│
├── .env                  # 환경 변수 (버전 관리에 포함시키지 말 것)
├── main.py               # 애플리케이션 진입점
├── requirements.txt      # 프로젝트 의존성
└── README.md             # 프로젝트 문서
```

## API 엔드포인트

### 인증

- `POST /api/v1/auth/signup`: 회원가입
- `POST /api/v1/auth/login`: 로그인

### 사용자

- `GET /api/v1/users/me`: 내 정보 조회
- `PUT /api/v1/users/me`: 내 정보 수정
- `GET /api/v1/users/{user_id}`: 특정 사용자 정보 조회
- `POST /api/v1/users/{user_id}/follow`: 사용자 팔로우
- `DELETE /api/v1/users/{user_id}/follow`: 사용자 언팔로우
- `GET /api/v1/users/{user_id}/followers`: 사용자의 팔로워 목록
- `GET /api/v1/users/{user_id}/following`: 사용자가 팔로우하는 목록

### 게시물

- `POST /api/v1/posts/`: 게시물 작성
- `GET /api/v1/posts/`: 피드 게시물 목록
- `GET /api/v1/posts/{post_id}`: 게시물 상세 조회
- `PUT /api/v1/posts/{post_id}`: 게시물 수정
- `DELETE /api/v1/posts/{post_id}`: 게시물 삭제
- `POST /api/v1/posts/{post_id}/like`: 게시물 좋아요
- `DELETE /api/v1/posts/{post_id}/like`: 게시물 좋아요 취소
- `GET /api/v1/posts/user/{user_id}`: 특정 사용자의 게시물 목록

### 댓글

- `POST /api/v1/comments/{post_id}`: 댓글 작성
- `GET /api/v1/comments/{post_id}`: 게시물의 댓글 목록
- `PUT /api/v1/comments/{comment_id}`: 댓글 수정
- `DELETE /api/v1/comments/{comment_id}`: 댓글 삭제

### 프로필

- `GET /api/v1/profile/me`: 내 프로필 조회
- `GET /api/v1/profile/me/posts`: 내 게시물 목록
- `GET /api/v1/profile/me/followers`: 내 팔로워 목록
- `GET /api/v1/profile/me/following`: 내가 팔로우하는 목록
- `GET /api/v1/profile/{user_id}`: 특정 사용자 프로필 조회

## 라이선스

이 프로젝트는 MIT 라이선스를 따릅니다.

## 기여

이슈와 풀 리퀘스트는 언제든지 환영합니다!
