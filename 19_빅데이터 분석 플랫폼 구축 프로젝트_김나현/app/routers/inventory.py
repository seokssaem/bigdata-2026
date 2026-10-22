from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.services import inventory_repo, inventory_service


router = APIRouter(prefix="/inventory", tags=["inventory"])


def to_inventory_read(item):
    return schemas.InventoryRead(
        product_id=item.product_id,
        sku=item.product.sku,
        name=item.product.name,
        quantity=item.quantity,
        reorder_point=item.product.reorder_point,
        needs_reorder=item.quantity <= item.product.reorder_point,
    )


@router.get("", response_model=list[schemas.InventoryRead])
def list_inventory(low_stock_only: bool = False, db: Session = Depends(get_session)):
    return [to_inventory_read(item) for item in inventory_repo.list(db, low_stock_only)]


@router.patch("/{product_id}", response_model=schemas.InventoryRead)
def adjust_stock(
    product_id: int,
    data: schemas.StockAdjustment,
    db: Session = Depends(get_session),
):
    return to_inventory_read(inventory_service.adjust(db, product_id, data.amount))

