from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.services import product_service


router = APIRouter(prefix="/products", tags=["products"])


@router.post("", response_model=schemas.ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: schemas.ProductCreate, db: Session = Depends(get_session)):
    return product_service.to_read(product_service.create(db, data))


@router.get("", response_model=list[schemas.ProductRead])
def list_products(
    search: str | None = None,
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_session),
):
    return [product_service.to_read(item) for item in product_service.list(db, search, skip, limit)]

