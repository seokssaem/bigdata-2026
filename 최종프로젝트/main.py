"""
FastAPI 앱 진입점

실행: uv run uvicorn main:app --reload
문서 확인: http://localhost:8000/docs
화면 확인: http://localhost:8000/
"""
import os

from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.sessions import SessionMiddleware

from database import Base, engine
import models  # noqa: F401  (모델을 불러와야 create_all 이 users/favorites 테이블도 만든다)
from routers import products, prices, predictions, pages, charts, auth, favorites
from templates_config import templates

# 아직 없는 테이블(users, favorites)만 만든다. 이미 있는 테이블과 데이터는 건드리지 않는다.
Base.metadata.create_all(bind=engine)

app = FastAPI(title="생필품 가격 리포트 API")

# 로그인 상태를 기억하는 쿠키(세션)에 서명할 비밀 문자열. 배포할 때는 반드시 .env/환경변수로 따로 설정한다.
SESSION_SECRET = os.getenv("SESSION_SECRET", "dev-only-secret-change-me")
app.add_middleware(
    SessionMiddleware,
    secret_key=SESSION_SECRET,
    max_age=60 * 60 * 24 * 14,  # 로그인 유지 기간: 14일
    same_site="lax",            # 다른 사이트에서 몰래 요청을 보내는 것(CSRF)을 막아준다
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """브라우저로 없는 페이지에 들어오면 JSON 대신 안내 화면을 보여준다.
    (API/이미지 요청은 Accept 헤더가 달라서 기존처럼 JSON으로 응답)"""
    if exc.status_code == 404 and "text/html" in request.headers.get("accept", ""):
        return templates.TemplateResponse(request, "404.html", {"active": ""}, status_code=404)
    return await http_exception_handler(request, exc)


# 화면(HTML) 라우터
app.include_router(pages.router)
app.include_router(auth.router)
app.include_router(charts.router)

# JSON API 라우터
app.include_router(favorites.router)
app.include_router(products.router)
app.include_router(prices.router)
app.include_router(predictions.router)
