'''
repositories/movie_repository.py

Movie(카탈로그) 테이블에 대한 DB쿼리만 담당. 전부 팀원 A(조회) 담당 영역.
카탈로그는 조회 전용으로 쓰므로 save/delete는 이 파일에 없음
(카탈로그 자체를 채우는 건 KOBIS 연동 스크립트나 load_data.py가 담당).
'''
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload
from models import Movie


class MovieRepository:
    def __init__(self, session: Session):
        self.session = session

    # ------------------ 조회 (팀원 A 담당 영역) ------------------
    def find_all(
        self,
        genre: str | None = None,
        nation: str | None = None,
        keyword: str | None = None,
        limit: int = 20,
        offset: int = 0,
    ) -> list[Movie]:
        stmt = select(Movie)
        if genre:
            stmt = stmt.where(Movie.genre.ilike(f'%{genre}%'))
        if nation:
            stmt = stmt.where(Movie.nation.ilike(f'%{nation}%'))
        if keyword:
            stmt = stmt.where(Movie.movie_nm.ilike(f'%{keyword}%'))
        stmt = stmt.limit(limit).offset(offset)
        return list(self.session.execute(stmt).scalars().all())

    def find_by_id(self, movie_cd: str) -> Movie | None:
        stmt = (
            select(Movie)
            .where(Movie.movie_cd == movie_cd)
            .options(selectinload(Movie.directors), selectinload(Movie.actors))
        )
        return self.session.execute(stmt).scalars().first()

    def count_all(self, genre: str | None = None, nation: str | None = None, keyword: str | None = None) -> int:
        stmt = select(Movie)
        if genre:
            stmt = stmt.where(Movie.genre.ilike(f'%{genre}%'))
        if nation:
            stmt = stmt.where(Movie.nation.ilike(f'%{nation}%'))
        if keyword:
            stmt = stmt.where(Movie.movie_nm.ilike(f'%{keyword}%'))
        return len(list(self.session.execute(stmt).scalars().all()))

    def exists(self, movie_cd: str) -> bool:
        return self.session.get(Movie, movie_cd) is not None

    # ------------------ KOBIS에서 가져온 영화를 카탈로그에 저장 ------------------
    def save(self, movie: Movie) -> Movie:
        self.session.add(movie)
        self.session.commit()
        self.session.refresh(movie)
        return movie
