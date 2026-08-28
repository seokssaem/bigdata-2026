'''
schema/request.py

- FavoriteCreateRequest: 즐겨찾기 추가 (팀원 B 담당) - movie_cd만 있으면 됨, 카탈로그의 영화를 참조
- FavoriteUpdateRequest: 즐겨찾기 메모 수정 (팀원 C 담당)
- MovieCreateRequest: 카탈로그에 영화를 직접 추가할 때 사용 (KOBIS 연동 없이 수동 등록하고 싶을 때 대비해 남겨둠)
'''
from pydantic import BaseModel, Field


class FavoriteCreateRequest(BaseModel):
    """POST /favorites 요청 body - 팀원 B 담당"""
    movie_cd: str = Field(..., description='즐겨찾기할 영화의 movie_cd (카탈로그에 이미 있어야 함)')
    memo: str | None = Field(None, description='즐겨찾기하며 남기는 메모 (선택)')


class FavoriteUpdateRequest(BaseModel):
    """PATCH /favorites/{id} 요청 body - 팀원 C 담당"""
    memo: str | None = None


class MovieCreateRequest(BaseModel):
    """POST /movies 요청 body - 카탈로그에 영화를 직접 등록할 때 (KOBIS 연동 전 임시 방편 또는 관리자용)"""
    movie_cd: str = Field(..., description='영화 코드 (KOBIS 코드 또는 직접 부여)')
    movie_nm: str = Field(..., description='영화명')
    movie_nm_en: str | None = None
    prdt_year: int | None = None
    open_dt: str | None = Field(None, description='YYYYMMDD 형식')
    show_tm: int | None = None
    prdt_stat_nm: str | None = None
    type_nm: str | None = None
    nation: str | None = None
    genre: str | None = None
    watch_grade: str | None = None
    directors: list[str] = []
    actors: list[str] = []
