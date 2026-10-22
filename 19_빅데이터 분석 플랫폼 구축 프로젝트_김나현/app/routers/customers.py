from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.services import customer_repo, customer_service


router = APIRouter(prefix="/customers", tags=["customers"])


@router.post("", response_model=schemas.CustomerRead, status_code=status.HTTP_201_CREATED)
def create_customer(data: schemas.CustomerCreate, db: Session = Depends(get_session)):
    return customer_service.create(db, data)


@router.get("", response_model=list[schemas.CustomerRead])
def list_customers(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    db: Session = Depends(get_session),
):
    return customer_repo.list(db, skip, limit)

