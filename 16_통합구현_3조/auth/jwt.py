# =========================================================================
# auth/jwt.py
#
# - JWT(JSON Web Token) 발급과 검증을 담당하는 모듈
# =========================================================================
import os
import jwt
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv('JWT_SECRET', 'change-this-secret-in-production')
ALGORITHM = 'HS256'  # HMAC-SHA256 서명 알고리즘

DEMO_USERNAME = os.getenv('DEMO_USERNAME', 'admin')
DEMO_PASSWORD = os.getenv('DEMO_PASSWORD', 'admin1234')

# /docs 우측 상단 Authorize 버튼이 토큰을 어디서 받아올지 알려주는 설정
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/users/login')


def create_access_token(username: str, expires_minutes: int = 60) -> str:
    """
    로그인에 성공한 사용자의 username을 담아 토큰 문자열을 발급한다.
    """
    payload = {
        'username': username,
        'exp': datetime.now(timezone.utc) + timedelta(minutes=expires_minutes),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def decode_access_token(token: str) -> str:
    """
    토큰을 검증하고, 그 안에 담겨있던 username만 뽑아서 반환한다.
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload['username']
    except jwt.ExpiredSignatureError:
        # 서명은 정상인데 exp(만료시간)이 지난 경우
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='토큰이 만료되었습니다',
        )
    except jwt.InvalidTokenError:
        # 서명이 위조됐거나 토큰 형식 자체가 잘못된 경우
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='유효하지 않은 토큰입니다',
        )


def authenticate_demo_user(username: str, password: str) -> bool:
    """
    회원 테이블 없이 .env에 정의한 고정 계정 1개로만 로그인 가능 (실습용 최소 구현)
    """
    return username == DEMO_USERNAME and password == DEMO_PASSWORD


def get_current_username(token: str = Depends(oauth2_scheme)) -> str:
    """
    쓰기(POST/PUT/DELETE) 라우터에서 Depends(get_current_username)으로 사용.
    토큰이 없거나 유효하지 않으면 자동으로 401을 반환한다.
    """
    return decode_access_token(token)
