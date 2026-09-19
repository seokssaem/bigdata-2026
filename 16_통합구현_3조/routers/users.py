# ==================================================================================
# routers/users.py
# - 로그인(JWT 발급) 라우터
# ==================================================================================
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from auth.jwt import authenticate_demo_user, create_access_token
from schema.response import TokenResponse

router = APIRouter(tags=['User'])


# 로그인 --> POST /users/login 요청이 오면 실행된다.
@router.post('/users/login', response_model=TokenResponse)
def login_handler(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    /docs 우측 상단 Authorize 버튼에서 이 계정으로 로그인하면
    쓰기(POST/PUT/DELETE) API를 눌러볼 수 있다.
    demo 계정: admin / admin1234 (.env에서 변경 가능)
    """
    if not authenticate_demo_user(form_data.username, form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='아이디 또는 비밀번호가 올바르지 않습니다',
        )
    token = create_access_token(form_data.username)
    return TokenResponse(access_token=token)
