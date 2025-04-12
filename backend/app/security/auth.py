import os
from datetime import datetime, timedelta, timezone
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT setup
SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = "HS256"

def get_password_hash(password):
    if not password:
        raise ValueError("비밀번호가 제공되지 않았습니다")
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    if not plain_password or not hashed_password:
        print(f"비밀번호 검증 오류: 비밀번호 또는 해시가 비어있습니다. plain_password={bool(plain_password)}, hashed_password={bool(hashed_password)}")
        return False
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"비밀번호 검증 중 예외 발생: {str(e)}")
        return False

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# 표준 OAuth2PasswordBearer 클래스 사용
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        # sub 값을 정수로 변환합니다
        try:
            user_id = int(user_id)
        except ValueError:
            raise HTTPException(status_code=401, detail="Invalid token format")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")