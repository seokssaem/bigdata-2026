from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.forecast_service import forecast_service

router = APIRouter(prefix="/forecasts", tags=["forecasts"])

@router.get('', response_model=schemas.ForecastOverview)
def forecast_all_products(
    weeks: int=Query(default=4, ge=1, le=12, description='앞으로 몇 주를 예측할지'),
    history_weeks: int=Query(default=12, ge=0, le=52, description='함께 보여줄 최근 실적 주 수'),
    db: Session = Depends(get_session)
):
    return forecast_service.overview(db, weeks, history_weeks)

@router.get('/products/{product_id}', response_model=schemas.ProductForecast)
def forecast_product(
    product_id: int, 
    weeks: int=Query(default=4, ge=1, le=12, description='앞으로 몇 주를 예측할지'),
    history_weeks: int=Query(default=12, ge=0, le=52, description='함께 보여줄 최근 실적 주 수'),
    db: Session = Depends(get_session)
):
    return forecast_service.for_product(db, product_id, weeks, history_weeks)