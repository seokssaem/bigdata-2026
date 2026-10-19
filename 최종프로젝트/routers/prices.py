"""등락률 랭킹 API - 최신 조사시점 기준 상승/하락 TOP N"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func

from database import get_db
import models
from schemas.price import PriceChangeOut

router = APIRouter(prefix="/prices", tags=["prices"])


@router.get("/trending", response_model=list[PriceChangeOut])
def get_trending_prices(
    direction: str = Query(default="up", pattern="^(up|down)$", description="up=상승 랭킹, down=하락 랭킹"),
    basis: str = Query(default="prev", pattern="^(prev|yoy)$", description="prev=직전대비, yoy=전년동기대비"),
    limit: int = Query(default=10, ge=1, le=50),
    category: str | None = Query(default=None),
    db: Session = Depends(get_db),
):
    """가장 최근 조사시점 기준으로, 등락률 상위/하위 상품을 반환."""
    latest_date = db.query(func.max(models.PriceChange.survey_date)).scalar()

    rate_col = models.PriceChange.change_rate if basis == "prev" else models.PriceChange.yoy_change_rate

    query = (
        db.query(models.PriceChange)
        .options(joinedload(models.PriceChange.product))
        .join(models.Product)
        .filter(models.PriceChange.survey_date == latest_date)
        .filter(rate_col.isnot(None))
    )
    if category:
        query = query.filter(models.Product.category == category)

    query = query.order_by(rate_col.desc() if direction == "up" else rate_col.asc())
    rows = query.limit(limit).all()

    return [
        PriceChangeOut(
            product_name=r.product.product_name,
            category=r.product.category,
            survey_date=r.survey_date,
            avg_price=r.avg_price,
            prev_price=r.prev_price,
            price_diff=r.price_diff,
            change_rate=r.change_rate,
            yoy_price=r.yoy_price,
            yoy_diff=r.yoy_diff,
            yoy_change_rate=r.yoy_change_rate,
        )
        for r in rows
    ]
