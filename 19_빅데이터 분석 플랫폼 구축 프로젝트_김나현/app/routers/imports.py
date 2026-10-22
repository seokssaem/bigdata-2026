from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from sqlalchemy.orm import Session

from app import schemas
from app.database import get_session
from app.import_service import import_service

router = APIRouter(prefix='/imports', tags=['imports'])

MAX_UPLOAD_BYTES = 10 * 1024 * 1024

@router.post('/orders', response_model=schemas.OrderImportResult, status_code=status.HTTP_201_CREATED)
def import_orders(
    file: UploadFile = File(..., description='주문 내역 CSV'),
    initial_stock: int = Query(default=0, ge=0, description='CSV로 새로 생성되는 상품의 시작 재고'),
    db: Session = Depends(get_session)
):
    content = file.file.read(MAX_UPLOAD_BYTES + 1)
    if len(content) > MAX_UPLOAD_BYTES:
        raise HTTPException(status.HTTP_413_CONTENT_TOO_LARGE, detail='파일은 10MB 이하여야 합니다.')
    return import_service.import_orders(db, content, initial_stock)