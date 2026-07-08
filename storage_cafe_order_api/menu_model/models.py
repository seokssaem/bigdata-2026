# 2026. 7. 8. 카페 주문 미니 프로젝트
# menu 모델 (자연키 방식)

from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Menu(Base):
    __tablename__ = 'menu'

    메뉴코드 = Column(String(30), primary_key=True)
    메뉴명 = Column(String(50), nullable=False)
    가격 = Column(Integer, nullable=False) 

    def __repr__(self):
        return f'<Menu {self.메뉴코드} {self.메뉴명} {self.가격}>'