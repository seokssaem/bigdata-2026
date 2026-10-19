import os

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from sqlalchemy.orm import Session

import models
from database import get_db
from schemas.user import UserLogin
from services.password_service import verify_password

import jwt

from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from services.auth_service import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    decode_access_token,
)

router = APIRouter(
    prefix="/auth",
    tags=["auth"]
)

security = HTTPBearer(auto_error=False)

# 운영 환경(HTTPS)에서는 .env 에 COOKIE_SECURE=true 로 설정하세요.
COOKIE_SECURE = os.getenv("COOKIE_SECURE", "false").lower() == "true"
COOKIE_NAME = "access_token"

@router.post("/login")
def login(
    login_data: UserLogin,
    response: Response,
    db: Session = Depends(get_db)
):
    # 이메일로 사용자 찾기
    user = (
        db.query(models.User)
        .filter(models.User.email == login_data.email)
        .first()
    )

    # 사용자가 존재하지 않는 경우
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    # 비밀번호 확인
    if not verify_password(
        login_data.password,
        user.password
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    access_token = create_access_token(user.id)
    response.set_cookie(
        key=COOKIE_NAME,
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60  # 토큰 만료와 동일하게 쿠키도 만료
    )

    return {
        "message": "로그인 성공",
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email
        }
    }

def get_current_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    # 1. Authorization 헤더에서 JWT 확인
    token = credentials.credentials if credentials else None

    # 2. Authorization 헤더가 없으면 Cookie에서 JWT 확인
    if not token:
        token = request.cookies.get(COOKIE_NAME)

    # 3. 둘 다 없으면 인증 실패
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증이 필요합니다."
        )
    
    try:
        payload = decode_access_token(token)

        user_id = payload.get("sub")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="유효하지 않은 인증 토큰입니다."
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="인증 토큰이 만료되었습니다."
        )

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 인증 토큰입니다."
        )

    user = (
        db.query(models.User)
        .filter(models.User.id == int(user_id))
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="사용자를 찾을 수 없습니다."
        )

    return user

def get_optional_user(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """화면(HTML)용: 로그인하지 않았거나 토큰이 유효하지 않으면 예외 대신 None 반환"""
    try:
        return get_current_user(request, credentials, db)
    except HTTPException:
        return None

def require_login_page(user: models.User | None = Depends(get_optional_user)):
    """화면(HTML)용 로그인 가드: 비로그인 시 로그인 페이지로 303 리다이렉트"""
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_303_SEE_OTHER,
            detail="로그인이 필요합니다.",
            headers={"Location": "/views/login"}
        )
    return user


@router.post("/logout")
def logout(response: Response):
    """httpOnly 쿠키는 JS 로 지울 수 없으므로 서버에서 삭제"""
    response.delete_cookie(
        key=COOKIE_NAME,
        httponly=True,
        samesite="lax",
        secure=COOKIE_SECURE
    )
    return {"message": "로그아웃 되었습니다."}


@router.get("/me")
def get_me(
    current_user: models.User = Depends(get_current_user)
):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
        "profile_image": current_user.profile_image
    }