"""가격 예측 관련 Pydantic 스키마"""
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class PredictionOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    product_name: str
    category: str
    base_price: float
    predicted_price: float
    expected_change_rate: float
    predicted_at: datetime
