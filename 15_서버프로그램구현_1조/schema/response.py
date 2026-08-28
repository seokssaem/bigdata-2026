'''
schema/response.py - 서버가 돌려주는 데이터의 형태
'''
from pydantic import BaseModel, ConfigDict


class MovieSummaryResponse(BaseModel):
    """카탈로그 목록 조회용 - 가벼운 필드만 (팀원 A 담당)"""
    model_config = ConfigDict(from_attributes=True)

    movie_cd: str
    movie_nm: str
    open_dt: str | None
    genre: str | None
    nation: str | None
    watch_grade: str | None


class MovieListResponse(BaseModel):
    """카탈로그 목록 응답 - 전체 개수 포함 (팀원 A 담당)"""
    total: int
    items: list[MovieSummaryResponse]


class MovieDetailResponse(BaseModel):
    """카탈로그 상세 조회용 - 감독/배우 포함 (팀원 A 담당)"""
    model_config = ConfigDict(from_attributes=True)

    movie_cd: str
    movie_nm: str
    movie_nm_en: str | None
    prdt_year: int | None
    open_dt: str | None
    show_tm: int | None
    prdt_stat_nm: str | None
    type_nm: str | None
    nation: str | None
    genre: str | None
    watch_grade: str | None
    directors: list[str] = []
    actors: list[str] = []


class FavoriteResponse(BaseModel):
    """즐겨찾기 응답 - movie_nm까지 같이 보여줘서 목록에서 바로 알아보기 쉽게 함"""
    id: int
    movie_cd: str
    movie_nm: str
    memo: str | None
