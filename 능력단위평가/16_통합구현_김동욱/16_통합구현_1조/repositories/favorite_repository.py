'''
repositories/favorite_repository.py

Favorite(즐겨찾기) 테이블에 대한 DB쿼리만 담당.
"추가"는 팀원 B, "수정/삭제"는 팀원 C 담당 영역으로 나뉜다.
'''
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload
from models import Favorite


class FavoriteRepository:
    def __init__(self, session: Session):
        self.session = session

    # ------------------ 추가 (팀원 B 담당 영역) ------------------
    def save(self, favorite: Favorite) -> Favorite:
        self.session.add(favorite)
        self.session.commit()
        self.session.refresh(favorite)
        return favorite

    def exists_by_movie_cd(self, movie_cd: str) -> bool:
        """이미 즐겨찾기한 영화인지 확인 (중복 즐겨찾기 방지용)"""
        stmt = select(Favorite).where(Favorite.movie_cd == movie_cd)
        return self.session.execute(stmt).scalars().first() is not None

    # ------------------ 조회 (즐겨찾기 목록 보기 - 공용) ------------------
    def find_all(self) -> list[Favorite]:
        stmt = select(Favorite).options(joinedload(Favorite.movie))
        return list(self.session.execute(stmt).scalars().all())

    def find_by_id(self, favorite_id: int) -> Favorite | None:
        stmt = select(Favorite).where(Favorite.id == favorite_id).options(joinedload(Favorite.movie))
        return self.session.execute(stmt).scalars().first()

    # ------------------ 수정/삭제 (팀원 C 담당 영역) ------------------
    def delete(self, favorite: Favorite) -> None:
        self.session.delete(favorite)
        self.session.commit()
