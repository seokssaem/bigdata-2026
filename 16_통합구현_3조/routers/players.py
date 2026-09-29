# ==============================================================
# routers/players.py
# - '선수(Player)' 관련 API 엔드포인트 모음
# ==============================================================
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, asc, desc, or_
from starlette import status

from database.db_connection import SessionFactory
from models import Player, PlayerE
from schema.request import PlayerCreateRequest, PlayerUpdateRequest
from schema.response import PlayerResponse
from auth.jwt import get_current_username

router = APIRouter(tags=['Player'])

# 정렬 허용 컬럼 화이트리스트 (아무 문자열이나 order_by에 넣으면 위험해서 제한)
SORTABLE_COLUMNS = {'goals', 'assists', 'age', 'games', 'minutes', 'player'}


# GET /players --> 선수 목록 조회 (필터 + 정렬 + 페이지네이션)
@router.get('/players', response_model=list[PlayerResponse], status_code=status.HTTP_200_OK)
def get_players_handler(
    team: str | None = Query(None, description='국가대표팀 이름으로 필터 (예: 대한민국)'),
    position: str | None = Query(None, description='포지션 필터 (GK/DF/MF/FW)'),
    search: str | None = Query(None, description='선수 이름 부분 검색'),
    sort_by: str = Query('goals', description=f'정렬 기준: {sorted(SORTABLE_COLUMNS)}'),
    order: str = Query('desc', pattern='^(asc|desc)$'),
    limit: int = Query(20, ge=1, le=200),
    offset: int = Query(0, ge=0),
):
    if sort_by not in SORTABLE_COLUMNS:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f'sort_by는 {sorted(SORTABLE_COLUMNS)} 중 하나여야 합니다')

    session = SessionFactory()
    try:
        stmt = select(Player)
        if team:
            stmt = stmt.where(Player.team == team)
        if position:
            stmt = stmt.where(Player.position == position)
        if search:
            # playerse(영어) 테이블에서 매칭되는 players_id 목록
            en_match_ids = select(PlayerE.id).where(PlayerE.player.ilike(f'%{search}%'))

            stmt = stmt.where(
                or_(
                    Player.player.ilike(f'%{search}%'),
                    Player.id.in_(en_match_ids),
                )
            )
        sort_col = getattr(Player, sort_by)
        stmt = stmt.order_by(desc(sort_col) if order == 'desc' else asc(sort_col))
        stmt = stmt.offset(offset).limit(limit)

        players = session.execute(stmt).scalars().all()
        return players
    finally:
        session.close()


# GET /players/{player_id} --> 선수 상세 조회
@router.get('/players/{player_id}', response_model=PlayerResponse, status_code=status.HTTP_200_OK)
def get_player_handler(player_id: int):
    session = SessionFactory()
    try:
        stmt = select(Player).where(Player.id == player_id)
        player = session.execute(stmt).scalars().first()
        if player:
            return player
        raise HTTPException(status.HTTP_404_NOT_FOUND, '해당 선수를 찾을 수 없습니다')
    finally:
        session.close()


# POST /players --> 선수 추가 (로그인 필요)
@router.post('/players', response_model=PlayerResponse, status_code=status.HTTP_201_CREATED)
def create_player_handler(body: PlayerCreateRequest, current_user: str = Depends(get_current_username)):
    session = SessionFactory()
    try:
        player = Player(**body.model_dump())
        session.add(player)
        session.commit()
        session.refresh(player)
        return player
    finally:
        session.close()


# PUT /players/{player_id} --> 선수 정보 수정 (로그인 필요, 보낸 필드만 반영)
@router.put('/players/{player_id}', response_model=PlayerResponse, status_code=status.HTTP_200_OK)
def update_player_handler(
    player_id: int,
    body: PlayerUpdateRequest,
    current_user: str = Depends(get_current_username),
):
    session = SessionFactory()
    try:
        stmt = select(Player).where(Player.id == player_id)
        player = session.execute(stmt).scalars().first()
        if not player:
            raise HTTPException(status.HTTP_404_NOT_FOUND, '해당 선수를 찾을 수 없습니다')

        # None이 아닌, 실제로 보낸 필드만 업데이트 (부분 수정 가능)
        update_data = body.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(player, key, value)

        session.commit()
        session.refresh(player)
        return player
    finally:
        session.close()


# DELETE /players/{player_id} --> 선수 삭제 (로그인 필요)
@router.delete('/players/{player_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_player_handler(player_id: int, current_user: str = Depends(get_current_username)):
    session = SessionFactory()
    try:
        stmt = select(Player).where(Player.id == player_id)
        player = session.execute(stmt).scalars().first()
        if not player:
            raise HTTPException(status.HTTP_404_NOT_FOUND, '해당 선수를 찾을 수 없습니다')
        session.delete(player)
        session.commit()
        return
    finally:
        session.close()
