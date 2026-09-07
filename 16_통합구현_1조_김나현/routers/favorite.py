'''
routers/favorite.py

즐겨찾기 엔드포인트.
- POST /favorites            : 팀원 B 담당
- GET /favorites             : 공용 (목록 화면 표시용)
- PATCH /favorites/{id}      : 팀원 C 담당
- DELETE /favorites/{id}     : 팀원 C 담당
'''
from fastapi import APIRouter, Depends
from starlette import status
from database.db_connection import get_session
from repositories.favorite_repository import FavoriteRepository
from repositories.movie_repository import MovieRepository
from services.favorite_service import FavoriteService
from schema.request import FavoriteCreateRequest, FavoriteUpdateRequest
from schema.response import FavoriteResponse

router = APIRouter(prefix='/favorites', tags=['Favorite'])


def get_favorite_service(session=Depends(get_session)) -> FavoriteService:
    return FavoriteService(FavoriteRepository(session), MovieRepository(session))


# ------------------ 조회 (공용) ------------------
@router.get('', response_model=list[FavoriteResponse], status_code=status.HTTP_200_OK)
def get_favorites_handler(service: FavoriteService = Depends(get_favorite_service)):
    return service.get_favorites()


# ------------------ 추가 (팀원 B 담당) ------------------
@router.post('', response_model=FavoriteResponse, status_code=status.HTTP_201_CREATED)
def add_favorite_handler(
    body: FavoriteCreateRequest,
    service: FavoriteService = Depends(get_favorite_service),
):
    return service.add_favorite(body)


# ------------------ 수정/삭제 (팀원 C 담당) ------------------
@router.patch('/{favorite_id}', response_model=FavoriteResponse, status_code=status.HTTP_200_OK)
def update_favorite_handler(
    favorite_id: int,
    body: FavoriteUpdateRequest,
    service: FavoriteService = Depends(get_favorite_service),
):
    return service.update_favorite(favorite_id, body)


@router.delete('/{favorite_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_favorite_handler(
    favorite_id: int,
    service: FavoriteService = Depends(get_favorite_service),
):
    service.delete_favorite(favorite_id)
