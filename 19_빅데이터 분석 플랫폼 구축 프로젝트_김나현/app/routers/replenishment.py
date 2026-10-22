from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.replenishment_service import replenishment_service

router = APIRouter(prefix="/replenishment", tags=["replenishment"])


@router.get("", response_model=schemas.ReplenishmentOverview)
def get_replenishment(
    lead_time_days: int = Query(default=7, ge=0, le=28, description="발주 후 입고까지 걸리는 일수(리드타임)"),
    cover_days: int = Query(default=14, ge=1, le=28, description="이번 발주로 커버하고 싶은 일수"),
    service_level: float = Query(default=0.95, ge=0.5, le=0.99, description="품절을 피하고 싶은 확률 (안전재고 계산용)"),
    needs_order_only: bool = Query(default=False, description="발주가 필요한 상품만 보기"),
    db: Session = Depends(get_session),
):
    return replenishment_service.overview(db, lead_time_days, cover_days, service_level, needs_order_only)
