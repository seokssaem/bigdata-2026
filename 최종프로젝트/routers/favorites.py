"""즐겨찾기 추가/해제 API (로그인한 회원만 사용 가능)

  POST /api/favorites/toggle   {"product_name": "상품명"}
    → 즐겨찾기에 없으면 추가, 있으면 해제. 결과 {"favorite": true/false}
    → 로그인 안 했으면 401 (화면의 favorites.js 가 로그인 화면으로 보내준다)
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
import models
from security import get_current_user

router = APIRouter(prefix="/api/favorites", tags=["favorites"])


class ToggleIn(BaseModel):
    product_name: str


@router.post("/toggle")
def toggle_favorite(
    body: ToggleIn,
    user: models.User | None = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if user is None:
        raise HTTPException(status_code=401, detail="로그인이 필요합니다.")

    product = db.query(models.Product).filter_by(product_name=body.product_name).first()
    if product is None:
        raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")

    favorite = db.query(models.Favorite).filter_by(user_id=user.id, product_id=product.id).first()
    if favorite:
        db.delete(favorite)
        db.commit()
        return {"favorite": False}

    db.add(models.Favorite(user_id=user.id, product_id=product.id))
    try:
        db.commit()
    except IntegrityError:  # 버튼을 아주 빠르게 두 번 눌러 이미 추가된 경우 → 추가된 상태 그대로 둔다
        db.rollback()
    return {"favorite": True}
