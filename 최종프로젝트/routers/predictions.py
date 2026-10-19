"""가격 예측 랭킹 API - 다음 조사시점 예상 상승/하락 TOP N"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload

from database import get_db
import models
from schemas.prediction import PredictionOut

router = APIRouter(prefix="/predictions", tags=["predictions"])


@router.get("", response_model=list[PredictionOut])
def get_predictions(
    direction: str = Query(default="up", pattern="^(up|down)$", description="up=상승예상, down=하락예상"),
    limit: int = Query(default=10, ge=1, le=50),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """다음 조사시점 기준 예상 등락률 상위/하위 상품을 반환."""
    query = (
        db.query(models.Prediction)
        .options(joinedload(models.Prediction.product))
        .join(models.Product)
    )
    if category:
        query = query.filter(models.Product.category == category)

    col = models.Prediction.expected_change_rate
    raw_col = models.Prediction.raw_expected_change_rate  # 상한 적용 전 값 (같은 값끼리 순서 정할 때 사용)
    if direction == "up":
        query = query.order_by(col.desc(), raw_col.desc())
    else:
        query = query.order_by(col.asc(), raw_col.asc())
    rows = query.limit(limit).all()

    return [
        PredictionOut(
            product_name=r.product.product_name,
            category=r.product.category,
            base_price=r.base_price,
            predicted_price=r.predicted_price,
            expected_change_rate=r.expected_change_rate,
            predicted_at=r.predicted_at,
        )
        for r in rows
    ]
