"""등락률 랭킹 관련 Pydantic 스키마"""
from datetime import date
from pydantic import BaseModel, ConfigDict


class PriceChangeOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str
    category: str
    survey_date: date
    avg_price: float
    prev_price: float | None
    price_diff: float | None
    change_rate: float | None
    yoy_price: float | None
    yoy_diff: float | None
    yoy_change_rate: float | None
