from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.services import order_repo, order_service


router = APIRouter(prefix="/orders", tags=["orders"])


@router.post("", response_model=schemas.OrderRead, status_code=status.HTTP_201_CREATED)
def create_order(data: schemas.OrderCreate, db: Session = Depends(get_session)):
    return order_service.to_read(order_service.create(db, data))


@router.get("", response_model=list[schemas.OrderRead])
def list_orders(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_session),
):
    return [order_service.to_read(order) for order in order_repo.list(db, skip, limit)]

