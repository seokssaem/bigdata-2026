# ================================================
# TEST/08_빅데이터저장시스템개발_김동욱/models.py
#
# 저장 모델 설계(스키마)
#
# 직접 실행되는 파일은 아니다. 
#   database.py, loader.py 가 import해서 사용
# ================================================
from sqlalchemy import Column, String, Integer, Numeric, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Water(Base):
    __tablename__ = "water"

    water_id = Column(Integer, primary_key=True, autoincrement=True)
    정수장 = Column(String(10), nullable=False)
    구분 = Column(String(10), nullable=False)
    ph = Column(Numeric(5, 2), nullable=False)
    탁도 = Column(Numeric(5, 2), nullable=False)
    잔류염소 = Column(Numeric(5, 2), nullable=False)
    검사시기 = Column(Date, nullable=False)
    
    __table_args__ = (
        UniqueConstraint("정수장", "구분", "검사시기", name="uq_water_key"),
    )


class Area(Base):
    __tablename__ = "area"

    area_id = Column(Integer, primary_key=True, autoincrement=True)
    정수장 = Column(String(10), nullable=False)
    구군 = Column(String(10), nullable=False)
    행정구역 = Column(String(10), nullable=False)
    급수분류 = Column(String(10), nullable=False)

    __table_args__ = (
        UniqueConstraint("정수장", "구군", "행정구역", "급수분류", name="uq_area_key"),
    )    