'''
=================================================================================
models.py

- Movie: KOBIS에서 가져온 영화 카탈로그 (조회 대상, 읽기 전용에 가까움)
- Actor / Director: 영화별 배우/감독 (1:N)
- Favorite: 사용자가 "찜"한 영화 목록 (movie_cd 참조 + 메모)
    -> 이제 "추가"는 새 영화를 만드는 게 아니라, 카탈로그에서 movie_cd를 골라
       Favorite에 등록하는 것. "수정/삭제"도 Favorite 대상으로 이루어진다.
=================================================================================
'''
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database.orm import Base


class Movie(Base):
    __tablename__ = 'movie'

    movie_cd: Mapped[str] = mapped_column(String(20), primary_key=True)  # KOBIS 영화 코드
    movie_nm: Mapped[str] = mapped_column(String(200), nullable=False)
    movie_nm_en: Mapped[str | None] = mapped_column(String(200), nullable=True)
    prdt_year: Mapped[int | None] = mapped_column(Integer, nullable=True)
    open_dt: Mapped[str | None] = mapped_column(String(8), nullable=True)  # YYYYMMDD, 결측 있어서 문자열
    show_tm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    prdt_stat_nm: Mapped[str | None] = mapped_column(String(20), nullable=True)
    type_nm: Mapped[str | None] = mapped_column(String(20), nullable=True)
    nation: Mapped[str | None] = mapped_column(String(100), nullable=True)
    genre: Mapped[str | None] = mapped_column(String(200), nullable=True)
    watch_grade: Mapped[str | None] = mapped_column(String(300), nullable=True)  # 등급 이력 여러 개 붙어 길어질 수 있음

    actors: Mapped[list['Actor']] = relationship(back_populates='movie', cascade='all, delete-orphan')
    directors: Mapped[list['Director']] = relationship(back_populates='movie', cascade='all, delete-orphan')


class Actor(Base):
    __tablename__ = 'actor'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_cd: Mapped[str] = mapped_column(ForeignKey('movie.movie_cd'), nullable=False)
    actor_name: Mapped[str] = mapped_column(String(100), nullable=False)

    movie: Mapped['Movie'] = relationship(back_populates='actors')


class Director(Base):
    __tablename__ = 'director'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_cd: Mapped[str] = mapped_column(ForeignKey('movie.movie_cd'), nullable=False)
    director_name: Mapped[str] = mapped_column(String(100), nullable=False)

    movie: Mapped['Movie'] = relationship(back_populates='directors')


class Favorite(Base):
    __tablename__ = 'favorite'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    movie_cd: Mapped[str] = mapped_column(ForeignKey('movie.movie_cd'), nullable=False)
    memo: Mapped[str | None] = mapped_column(String(200), nullable=True)  # 즐겨찾기하며 남기는 메모 (선택)

    movie: Mapped['Movie'] = relationship()
