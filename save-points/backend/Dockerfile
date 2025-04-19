# Python 3.12 이미지를 기반으로 합니다
FROM python:3.12-slim

# 작업 디렉토리 설정
WORKDIR /app

# 필요한 패키지 설치를 위한 파일 복사
COPY requirements.txt .

# 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY . .

# 컨테이너 내부에서 사용할 포트 설정
EXPOSE 8000

# 환경 변수 설정 (기본값)
ENV DATABASE_URL=sqlite:///threads_app.db

# 애플리케이션 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]