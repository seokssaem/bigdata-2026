"""
SQLAlchemy ORM 모델

products         - 상품 기본정보 (상품명, 카테고리)
price_history    - 상품×조사일 평균가격 (시계열의 원본)
price_changes    - 등락률 계산 결과 (직전대비, 전년동기대비)
predictions      - 다음 조사시점 가격 예측 결과
users            - 회원 (아이디, 암호화된 비밀번호)
favorites        - 회원별 즐겨찾기 (user_id, product_id)
"""
from sqlalchemy import (
    Column, Integer, String, Float, Date, DateTime, ForeignKey, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(200), unique=True, nullable=False, index=True)
    category = Column(String(50), nullable=False, default="기타 가공식품")

    price_history = relationship("PriceHistory", back_populates="product")
    price_changes = relationship("PriceChange", back_populates="product")
    prediction = relationship("Prediction", back_populates="product", uselist=False)


class PriceHistory(Base):
    """상품×조사일 평균가격 (등락률 계산의 원본이 되는 시계열 데이터)"""
    __tablename__ = "price_history"
    __table_args__ = (UniqueConstraint("product_id", "survey_date", name="uq_product_date"),)

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    survey_date = Column(Date, nullable=False, index=True)
    avg_price = Column(Float, nullable=False)

    product = relationship("Product", back_populates="price_history")


class PriceChange(Base):
    """등락률 계산 결과 (analysis.py의 build_full_analysis 결과가 여기 적재됨)"""
    __tablename__ = "price_changes"
    __table_args__ = (UniqueConstraint("product_id", "survey_date", name="uq_change_product_date"),)

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    survey_date = Column(Date, nullable=False, index=True)

    avg_price = Column(Float, nullable=False)
    prev_price = Column(Float, nullable=True)
    price_diff = Column(Float, nullable=True)
    change_rate = Column(Float, nullable=True)          # 직전 대비 등락률(%)

    yoy_price = Column(Float, nullable=True)             # 전년동기 가격
    yoy_diff = Column(Float, nullable=True)
    yoy_change_rate = Column(Float, nullable=True)        # 전년동기 대비 등락률(%)

    product = relationship("Product", back_populates="price_changes")


class User(Base):
    """회원 정보. 비밀번호는 원문이 아니라 암호화(해시)한 값만 저장한다."""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    favorites = relationship("Favorite", back_populates="user", cascade="all, delete-orphan")


class Favorite(Base):
    """누가(user) 어떤 상품(product)을 즐겨찾기했는지. 같은 조합은 한 번만 저장된다."""
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_user_product"),)

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="favorites")
    product = relationship("Product")


class Prediction(Base):
    """다음 조사시점 가격 예측 결과 (predictor.py 결과가 여기 적재됨, 상품당 최신 1건 유지)"""
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), unique=True, nullable=False)

    base_price = Column(Float, nullable=False)
    predicted_price = Column(Float, nullable=False)
    expected_change_rate = Column(Float, nullable=False)       # 상한/하한 적용된 최종값
    raw_expected_change_rate = Column(Float, nullable=False)   # 보정 전 원본 예측값
    predicted_at = Column(DateTime, server_default=func.now())

    product = relationship("Product", back_populates="prediction")
