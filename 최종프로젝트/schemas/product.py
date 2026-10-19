"""상품/가격이력 관련 Pydantic 스키마"""
from datetime import date
from pydantic import BaseModel, ConfigDict


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_name: str
    category: str


class PriceHistoryOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    survey_date: date
    avg_price: float


class ProductDetailOut(BaseModel):
    """상품 상세 - 기본정보 + 전체 가격이력"""
    model_config = ConfigDict(from_attributes=True)
    id: int
    product_name: str
    category: str
    price_history: list[PriceHistoryOut]
