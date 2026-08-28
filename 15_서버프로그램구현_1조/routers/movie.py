'''
routers/movie.py - Movie 카탈로그 조회 엔드포인트 (팀원 A 담당)
'''
from fastapi import APIRouter, Depends, Query
from starlette import status
from database.db_connection import get_session
from repositories.movie_repository import MovieRepository
from services.movie_service import MovieService
from schema.request import MovieCreateRequest
from schema.response import MovieListResponse, MovieDetailResponse

router = APIRouter(prefix='/movies', tags=['Movie Catalog'])


def get_movie_service(session=Depends(get_session)) -> MovieService:
    return MovieService(MovieRepository(session))


@router.get('', response_model=MovieListResponse, status_code=status.HTTP_200_OK)
def get_movies_handler(
    genre: str | None = Query(None, description='장르 필터 (부분일치)'),
    nation: str | None = Query(None, description='국가 필터 (부분일치)'),
    keyword: str | None = Query(None, description='영화명 검색 (부분일치)'),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: MovieService = Depends(get_movie_service),
):
    return service.get_movies(genre, nation, keyword, limit, offset)


@router.get('/{movie_cd}', response_model=MovieDetailResponse, status_code=status.HTTP_200_OK)
def get_movie_detail_handler(
    movie_cd: str,
    service: MovieService = Depends(get_movie_service),
):
    return service.get_movie_detail(movie_cd)


@router.post('/ensure', status_code=status.HTTP_204_NO_CONTENT)
def ensure_movie_handler(
    body: MovieCreateRequest,
    service: MovieService = Depends(get_movie_service),
):
    """
    KOBIS에서 실시간으로 조회한 영화 정보를 카탈로그에 등록(이미 있으면 무시).
    즐겨찾기 버튼을 눌렀을 때 Streamlit이 이 엔드포인트를 먼저 호출한 뒤 POST /favorites를 호출한다.
    """
    service.create_movie_if_not_exists(body)
