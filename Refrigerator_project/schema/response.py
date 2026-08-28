'''
schema/response.py

응답 모델 정의
'''
from datetime import date
from pydantic import BaseModel
from typing import Optional

class IngredientResponse(BaseModel):
    id: int
    name: str
    category: str
    quantity: str
    purchase_date: date
    expiration_date: date
    storage_method: str

    class Config:
        from_attributes = True  # SQLAlchemy 객체를 Pydantic 변수로 자동 매핑해 주는 옵션