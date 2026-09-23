# =========================================================================
# main.py
# - FastAPI 애플리케이션의 진입점 (entry point)
# - 앱(app) 객체 생성, DB 테이블 생성, 라우터(Router) 등록을 담당하는 파일
# =========================================================================
from fastapi import FastAPI
from database.db_connection import engine
from database.orm import Base
from routers.players import router as players_router
from routers.matches import router as matches_router
from routers.teams import router as teams_router
from routers.stats import router as stats_router
from routers.users import router as users_router

# models.py의 클래스들을 Base에 등록시키기 위해 import (안 하면 create_all이 무시함)
import models  # noqa: F401

# 테이블이 이미 schema.sql로 만들어져 있으면(scripts/load_data.py 실행 후) 그냥 스킵되고,
# 없으면 models.py에 정의된 핵심 컬럼만으로 테이블을 새로 만든다.
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title='2026 FIFA 월드컵 데이터 API',
    description='PostgreSQL에 저장된 선수/경기/팀 데이터를 FastAPI로 조회·수정하는 실습 프로젝트',
)

# 라우터 등록
app.include_router(users_router)
app.include_router(players_router)
app.include_router(matches_router)
app.include_router(teams_router)
app.include_router(stats_router)


@app.get('/')
def root():
    return {
        'message': '2026 FIFA 월드컵 데이터 API',
        'docs': '/docs',
        'endpoints': ['/players', '/matches', '/teams', '/stats/top-scorers', '/stats/team-goal-diff'],
    }

@app.get("/health")
def health():
    return {
        "status": "ok"
    }