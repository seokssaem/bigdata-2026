"""상품 목록 조회, 상품 검색, 상품 상세(가격이력) API"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
import models
from schemas.product import ProductOut, ProductDetailOut

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductOut])
def list_products(
    category: str | None = Query(default=None, description="카테고리로 필터링"),
    search: str | None = Query(default=None, description="상품명 부분검색"),
    db: Session = Depends(get_db),
):
    """상품 목록 조회. category, search 파라미터로 필터링 가능."""
    query = db.query(models.Product)
    if category:
        query = query.filter(models.Product.category == category)
    if search:
        query = query.filter(models.Product.product_name.contains(search))
    return query.order_by(models.Product.product_name).all()


@router.get("/categories", response_model=list[str])
def list_categories(db: Session = Depends(get_db)):
    """존재하는 카테고리 목록만 뽑아서 반환 (필터 드롭다운용)."""
    rows = db.query(models.Product.category).distinct().order_by(models.Product.category).all()
    return [r[0] for r in rows]


@router.get("/{product_name}", response_model=ProductDetailOut)
def get_product_detail(product_name: str, db: Session = Depends(get_db)):
    """상품명으로 상세정보 + 전체 가격이력(시계열) 조회."""
    product = db.query(models.Product).filter_by(product_name=product_name).first()
    if product is None:
        raise HTTPException(status_code=404, detail=f"'{product_name}' 상품을 찾을 수 없습니다.")
    # 가격이력은 조사일 순으로 정렬해서 내려줌 (그래프 그릴 때 바로 쓰기 좋게)
    product.price_history.sort(key=lambda ph: ph.survey_date)
    return product
