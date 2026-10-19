"""회원가입 / 로그인 / 로그아웃 화면과 처리

  GET  /signup   가입 화면          POST /signup   가입 처리
  GET  /login    로그인 화면        POST /login    로그인 처리
  POST /logout   로그아웃 처리
"""
import re

from fastapi import APIRouter, Depends, Form, Request
from fastapi.responses import RedirectResponse
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
import models
from security import get_current_user, hash_password, login_session, safe_next, verify_password
from templates_config import templates

router = APIRouter(tags=["auth"])

# 아이디: 한글/영문/숫자/밑줄 3~20자
USERNAME_PATTERN = re.compile(r"^[A-Za-z0-9_가-힣]{3,20}$")
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def redirect(url: str) -> RedirectResponse:
    # 303: 폼을 POST로 보낸 뒤 결과 화면은 GET으로 열라는 뜻 (새로고침해도 폼이 다시 전송되지 않음)
    return RedirectResponse(url, status_code=303)


def render_form(request: Request, template: str, next_url: str, error: str | None = None,
                username: str = "", status_code: int = 200):
    return templates.TemplateResponse(request, template, {
        "active": "", "next": next_url, "error": error, "username": username,
    }, status_code=status_code)


# ──────────────────────────── 회원가입 ────────────────────────────

@router.get("/signup")
def signup_page(request: Request, next: str = "/", user: models.User | None = Depends(get_current_user)):
    if user:
        return redirect(safe_next(next))
    return render_form(request, "signup.html", safe_next(next))


@router.post("/signup")
def signup(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    password2: str = Form(""),
    next: str = Form("/"),
    db: Session = Depends(get_db),
):
    username = username.strip()
    next_url = safe_next(next)

    if not USERNAME_PATTERN.match(username):
        error = "아이디는 한글, 영문, 숫자, _ 로 3~20자까지 쓸 수 있어요."
    elif not (MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH):
        error = f"비밀번호는 {MIN_PASSWORD_LENGTH}자 이상으로 만들어주세요."
    elif password != password2:
        error = "비밀번호 확인이 일치하지 않아요."
    elif db.query(models.User).filter(func.lower(models.User.username) == username.lower()).first():
        error = "이미 사용 중인 아이디예요."
    else:
        error = None

    if error:
        return render_form(request, "signup.html", next_url, error, username, status_code=400)

    user = models.User(username=username, password_hash=hash_password(password))
    db.add(user)
    try:
        db.commit()
    except IntegrityError:  # 거의 동시에 같은 아이디로 가입한 경우
        db.rollback()
        return render_form(request, "signup.html", next_url, "이미 사용 중인 아이디예요.", username, 400)

    login_session(request, user)  # 가입하면 바로 로그인된 상태로
    return redirect(next_url)


# ──────────────────────────── 로그인 / 로그아웃 ────────────────────────────

@router.get("/login")
def login_page(request: Request, next: str = "/", user: models.User | None = Depends(get_current_user)):
    if user:
        return redirect(safe_next(next))
    return render_form(request, "login.html", safe_next(next))


@router.post("/login")
def login(
    request: Request,
    username: str = Form(""),
    password: str = Form(""),
    next: str = Form("/"),
    db: Session = Depends(get_db),
):
    username = username.strip()
    next_url = safe_next(next)

    user = db.query(models.User).filter(func.lower(models.User.username) == username.lower()).first()
    # 아이디가 없는지, 비밀번호가 틀린 건지 알려주지 않고 같은 문구로 답한다 (아이디 추측 방지)
    if user is None or not verify_password(password, user.password_hash):
        return render_form(request, "login.html", next_url,
                           "아이디 또는 비밀번호가 올바르지 않아요.", username, status_code=400)

    login_session(request, user)
    return redirect(next_url)


@router.post("/logout")
def logout(request: Request):
    request.session.clear()
    return redirect("/")
