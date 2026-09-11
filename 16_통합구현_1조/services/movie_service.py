'''
services/movie_service.py - Movie 카탈로그 조회 업무 로직 (팀원 A 담당)
'''
from fastapi import HTTPException, status
from models import Movie, Actor, Director
from repositories.movie_repository import MovieRepository
from schema.request import MovieCreateRequest
from schema.response import MovieDetailResponse, MovieListResponse


class MovieService:
    def __init__(self, repository: MovieRepository):
        self.repository = repository

    def get_movies(self, genre, nation, keyword, limit, offset) -> MovieListResponse:
        items = self.repository.find_all(genre, nation, keyword, limit, offset)
        total = self.repository.count_all(genre, nation, keyword)
        return MovieListResponse(total=total, items=items)

    def get_movie_detail(self, movie_cd: str) -> MovieDetailResponse:
        movie = self.repository.find_by_id(movie_cd)
        if movie is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='영화를 찾을 수 없습니다.')

        return MovieDetailResponse(
            movie_cd=movie.movie_cd,
            movie_nm=movie.movie_nm,
            movie_nm_en=movie.movie_nm_en,
            prdt_year=movie.prdt_year,
            open_dt=movie.open_dt,
            show_tm=movie.show_tm,
            prdt_stat_nm=movie.prdt_stat_nm,
            type_nm=movie.type_nm,
            nation=movie.nation,
            genre=movie.genre,
            watch_grade=movie.watch_grade,
            directors=[d.director_name for d in movie.directors],
            actors=[a.actor_name for a in movie.actors],
        )

    def create_movie_if_not_exists(self, body: MovieCreateRequest) -> None:
        """
        KOBIS에서 실시간으로 조회한 영화를 즐겨찾기하려면, 먼저 카탈로그(movie)에
        있어야 외래키 제약을 만족한다. 이미 있으면 그냥 넘어가고(에러 안 냄),
        없으면 새로 만든다. -> 즐겨찾기 흐름이 끊기지 않게 하기 위한 헬퍼.
        """
        if self.repository.exists(body.movie_cd):
            return

        movie = Movie(
            movie_cd=body.movie_cd,
            movie_nm=body.movie_nm,
            movie_nm_en=body.movie_nm_en,
            prdt_year=body.prdt_year,
            open_dt=body.open_dt,
            show_tm=body.show_tm,
            prdt_stat_nm=body.prdt_stat_nm,
            type_nm=body.type_nm,
            nation=body.nation,
            genre=body.genre,
            watch_grade=body.watch_grade,
        )
        movie.directors = [Director(director_name=name, movie_cd=body.movie_cd) for name in body.directors]
        movie.actors = [Actor(actor_name=name, movie_cd=body.movie_cd) for name in body.actors]
        self.repository.save(movie)
