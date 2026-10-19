"""
로그인에 필요한 도구 모음

- 비밀번호 암호화 / 확인  (hash_password, verify_password)
- 지금 로그인한 사람 찾기  (get_current_user)
- 로그인 후 돌아갈 주소 검사 (safe_next)

로그인 상태는 브라우저 쿠키(세션)에 "user_id"를 넣어서 기억한다.
쿠키는 main.py의 SessionMiddleware가 SESSION_SECRET으로 서명해서, 값을 몰래 바꾸면 무효가 된다.
"""
import hashlib
import hmac
import os

from fastapi import Depends, Request
from sqlalchemy.orm import Session

from database import get_db
import models

# 비밀번호를 섞고 반복해서 계산하는 횟수. 클수록 비밀번호를 무작정 대입해 맞추기 어려워진다.
ITERATIONS = 600_000


def hash_password(password: str) -> str:
    """비밀번호를 되돌릴 수 없는 값으로 바꿔서 'pbkdf2_sha256$횟수$소금$해시' 문자열로 돌려준다.

    사람마다 다른 무작위 값(salt, 소금)을 섞기 때문에,
    같은 비밀번호를 쓰는 두 사람도 저장되는 값이 서로 다르다.
    """
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, ITERATIONS)
    return f"pbkdf2_sha256${ITERATIONS}${salt.hex()}${digest.hex()}"


def verify_password(password: str, stored: str) -> bool:
    """입력한 비밀번호가 저장된 값과 맞는지 확인한다."""
    try:
        algorithm, iterations, salt_hex, digest_hex = stored.split("$")
        if algorithm != "pbkdf2_sha256":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256", password.encode("utf-8"), bytes.fromhex(salt_hex), int(iterations)
        )
    except (ValueError, TypeError):
        return False  # 저장 형식이 이상하면 그냥 "다름"으로 처리
    # 일반 == 대신 compare_digest: 비교 시간 차이로 값을 추측하는 공격을 막는다
    return hmac.compare_digest(digest.hex(), digest_hex)


def get_current_user(request: Request, db: Session = Depends(get_db)) -> models.User | None:
    """쿠키 세션에 기억된 user_id로 지금 로그인한 회원을 찾는다. 로그인 안 했으면 None."""
    user_id = request.session.get("user_id")
    if user_id is None:
        return None
    user = db.get(models.User, user_id)
    if user is None:  # 탈퇴/삭제 등으로 사라진 회원이면 세션도 비운다
        request.session.clear()
    return user


def login_session(request: Request, user: models.User) -> None:
    """로그인 처리: 이전 세션 내용을 지우고 이 회원으로 새로 기록한다."""
    request.session.clear()
    request.session["user_id"] = user.id
    request.session["username"] = user.username  # 화면 위쪽 메뉴에 이름을 보여주기 위해


def safe_next(target: str | None) -> str:
    """로그인 후 돌아갈 주소가 '이 사이트 안의 주소'일 때만 허용한다.

    ?next=https://나쁜사이트 처럼 밖으로 보내는 주소를 막기 위한 검사다.
    """
    if target and target.startswith("/") and not target.startswith("//") and "\\" not in target:
        return target
    return "/"
