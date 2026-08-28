'''
services/favorite_service.py

즐겨찾기 관련 업무 로직.
- 추가(add_favorite): 팀원 B 담당
- 수정/삭제(update_favorite, delete_favorite): 팀원 C 담당
- 조회(get_favorites): 공용 (목록 화면에서 필요하므로)
'''
from fastapi import HTTPException, status
from models import Favorite
from repositories.favorite_repository import FavoriteRepository
from repositories.movie_repository import MovieRepository
from schema.request import FavoriteCreateRequest, FavoriteUpdateRequest
from schema.response import FavoriteResponse


class FavoriteService:
    def __init__(self, favorite_repository: FavoriteRepository, movie_repository: MovieRepository):
        self.favorite_repository = favorite_repository
        self.movie_repository = movie_repository

    def _to_response(self, favorite: Favorite) -> FavoriteResponse:
        return FavoriteResponse(
            id=favorite.id,
            movie_cd=favorite.movie_cd,
            movie_nm=favorite.movie.movie_nm,
            memo=favorite.memo,
        )

    # ------------------ 조회 (공용) ------------------
    def get_favorites(self) -> list[FavoriteResponse]:
        favorites = self.favorite_repository.find_all()
        return [self._to_response(f) for f in favorites]

    # ------------------ 추가 (팀원 B 담당 영역) ------------------
    def add_favorite(self, body: FavoriteCreateRequest) -> FavoriteResponse:
        if not self.movie_repository.exists(body.movie_cd):
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='카탈로그에 없는 영화입니다.')

        if self.favorite_repository.exists_by_movie_cd(body.movie_cd):
            raise HTTPException(status.HTTP_409_CONFLICT, detail='이미 즐겨찾기한 영화입니다.')

        favorite = Favorite(movie_cd=body.movie_cd, memo=body.memo)
        saved = self.favorite_repository.save(favorite)
        return self._to_response(saved)

    # ------------------ 수정/삭제 (팀원 C 담당 영역) ------------------
    def update_favorite(self, favorite_id: int, body: FavoriteUpdateRequest) -> FavoriteResponse:
        favorite = self.favorite_repository.find_by_id(favorite_id)
        if favorite is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='즐겨찾기를 찾을 수 없습니다.')

        for field, value in body.model_dump(exclude_unset=True).items():
            setattr(favorite, field, value)

        saved = self.favorite_repository.save(favorite)
        return self._to_response(saved)

    def delete_favorite(self, favorite_id: int) -> None:
        favorite = self.favorite_repository.find_by_id(favorite_id)
        if favorite is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, detail='즐겨찾기를 찾을 수 없습니다.')
        self.favorite_repository.delete(favorite)
