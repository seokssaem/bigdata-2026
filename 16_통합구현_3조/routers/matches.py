# ==============================================================
# routers/matches.py
# - '경기(Match)' 조회 API 엔드포인트 모음
# ==============================================================
from fastapi import APIRouter, HTTPException, Query
from sqlalchemy import select
from starlette import status

from database.db_connection import SessionFactory
from models import Match
from schema.response import MatchResponse

router = APIRouter(tags=['Match'])


# GET /matches --> 경기 목록 조회 (팀/라운드/날짜 필터)
@router.get('/matches', response_model=list[MatchResponse], status_code=status.HTTP_200_OK)
def get_matches_handler(
    team: str | None = Query(None, description='홈팀 또는 원정팀으로 필터 (예: 대한민국)'),
    round: str | None = Query(None, description='라운드 필터 (예: 조별리그, 8강, 결승)'),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    session = SessionFactory()
    try:
        stmt = select(Match)
        if team:
            stmt = stmt.where((Match.home_team == team) | (Match.away_team == team))
        if round:
            stmt = stmt.where(Match.round == round)
        stmt = stmt.order_by(Match.date.asc(), Match.start_time.asc())
        stmt = stmt.offset(offset).limit(limit)

        matches = session.execute(stmt).scalars().all()
        return matches
    finally:
        session.close()


# GET /matches/{match_id} --> 경기 상세 조회
@router.get('/matches/{match_id}', response_model=MatchResponse, status_code=status.HTTP_200_OK)
def get_match_handler(match_id: int):
    session = SessionFactory()
    try:
        stmt = select(Match).where(Match.id == match_id)
        match = session.execute(stmt).scalars().first()
        if match:
            return match
        raise HTTPException(status.HTTP_404_NOT_FOUND, '해당 경기를 찾을 수 없습니다')
    finally:
        session.close()
