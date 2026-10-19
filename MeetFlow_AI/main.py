import os

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

import models
from database import Base, engine
from routers import auth, meetings, profile, projects, tasks, users, views


# ============================================================
# 데이터베이스 테이블 생성
# ============================================================

Base.metadata.create_all(bind=engine)


# ============================================================
# FastAPI 애플리케이션 생성
# ============================================================

app = FastAPI(
    title="MeetFlow AI",
    description="AI 기반 스마트 회의·업무 관리 플랫폼",
    version="0.1.0"
)


# ============================================================
# 필요한 디렉토리 생성
# ============================================================

os.makedirs("static", exist_ok=True)
os.makedirs("uploads", exist_ok=True)
os.makedirs("uploads/profile", exist_ok=True)
os.makedirs("data", exist_ok=True)


# ============================================================
# 정적 파일 및 업로드 파일 경로 등록
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

# 프로필 사진만 정적 공개합니다.
# 회의 녹음(uploads/audio)은 개인 정보이므로 공개하지 않고,
# 로그인 + 소유자 확인을 거치는 GET /meetings/{id}/audio 로만 제공합니다.
app.mount(
    "/uploads/profile",
    StaticFiles(directory="uploads/profile"),
    name="profile_images"
)


# ============================================================
# Router 등록
# ============================================================

app.include_router(users.router)
app.include_router(profile.router)
app.include_router(auth.router)
app.include_router(projects.router)
app.include_router(meetings.router)
app.include_router(tasks.router)
app.include_router(views.router)
app.add_api_route("/login", views.login_view, methods=["GET"], include_in_schema=False)


# ============================================================
# 기본 API
# ============================================================

@app.get("/")
def root():
    return {
        "message": "MeetFlow AI API",
        "status": "ok"
    }


# ============================================================
# 화면 진입 경로
# ============================================================

@app.get("/views", include_in_schema=False)
def redirect_to_views():
    return RedirectResponse(
        url="/views/dashboard"
    )