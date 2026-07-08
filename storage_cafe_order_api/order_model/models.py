# 2026. 7. 8. 카페 주문 미니 프로젝트
# orders 모델 (대체키 + UNIQUE 방식)

from sqlalchemy import Column, String, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, autoincrement= True)
    주문일시= Column(DateTime,nullable=False)
    테이블번호 = Column(Integer, nullable=False)
    메뉴코드 = Column(String(10), nullable=False)
    수량 = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint('테이블번호', '메뉴코드','수량', name='uq_orders_key'),)

    def __repr__(self):
        return f'<Order {self.주문일시} T{self.테이블번호} {self.메뉴코드} x{self.수량}>'