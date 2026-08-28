'''
models.py
-----------------------------
예광탄 방식을 활용한 아주 얇은 코드
스키마, 테이블 만들기 (ORM)
'''
from datetime import datetime, date
from sqlalchemy import DateTime, String, Date
from sqlalchemy.orm import Mapped, mapped_column
from database import Base

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), index=True)
    category: Mapped[str] = mapped_column(String(50), index=True)
    quantity: Mapped[str | None] = mapped_column(String(20))
    purchase_date: Mapped[date] = mapped_column(Date)
    expiration_date: Mapped[date] = mapped_column(Date, index=True)
    storage_method: Mapped[str] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<Ingredient(id={self.id}, name='{self.name}', category='{self.category})>"
