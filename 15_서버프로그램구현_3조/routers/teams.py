# ==============================================================
# routers/teams.py
# - '팀(Team)' 조회 API 엔드포인트 모음
# ==============================================================
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from starlette import status

from database.db_connection import SessionFactory
from models import Team
from schema.response import TeamResponse

router = APIRouter(tags=['Team'])


# GET /teams --> 팀 목록 조회 (이름 검색)
@router.get('/teams', response_model=list[TeamResponse], status_code=status.HTTP_200_OK)
def get_teams_handler(
    search: str | None = Query(None, description='팀 이름 부분 검색'),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
):
    session = SessionFactory()
    try:
        stmt = select(Team)
        if search:
            stmt = stmt.where(Team.team.ilike(f'%{search}%'))
        stmt = stmt.offset(offset).limit(limit)

        teams = session.execute(stmt).scalars().all()
        return teams
    finally:
        session.close()


# GET /teams/{team_id} --> 팀 상세 조회
@router.get('/teams/{team_id}', response_model=TeamResponse, status_code=status.HTTP_200_OK)
def get_team_handler(team_id: int):
    session = SessionFactory()
    try:
        stmt = select(Team).where(Team.id == team_id)
        team = session.execute(stmt).scalars().first()
        if team:
            return team
        raise HTTPException(status.HTTP_404_NOT_FOUND, '해당 팀을 찾을 수 없습니다')
    finally:
        session.close()
