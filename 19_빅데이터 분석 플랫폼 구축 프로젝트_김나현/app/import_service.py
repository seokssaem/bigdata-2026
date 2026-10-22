import csv
import io
from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.repositories import ImportRepository

import_repo = ImportRepository()

REQUIRED_COLUMNS = ["order_id", "ordered_at", "business_number", "company_name", "sku", "product_name", "quantity", "unit_price"]

@dataclass
class ParsedRow:
    order_key: str  # 같은 주문의 행들을 묶는 역할, 저장 X
    ordered_at: datetime
    business_number: str
    company_name: str
    sku: str
    product_name: str
    quantity: int
    unit_price: Decimal

class ImportService:
    def import_orders(self, db: Session, content: bytes, initial_stock: int=0) -> schemas.OrderImportResult:
        rows = self._parse_and_validate(content)

        customers = import_repo.get_customers_by_business_numbers(db, {r.business_number for r in rows})
        products = import_repo.get_products_by_skus(db, {r.sku for r in rows})

        new_customers: list[models.Customer] = []
        new_products: list[models.Product] = []

        for r in rows:
            if r.business_number not in customers:
                customer = models.Customer(company_name=r.company_name, business_number=r.business_number)
                customers[r.business_number] = customer
                new_customers.append(customer)

            if r.sku not in products:
                product = models.Product(sku=r.sku, name=r.product_name, unit_price=r.unit_price)
                product.inventory = models.Inventory(quantity=initial_stock)
                products[r.sku] = product
                new_products.append(product)

        # order_id가 같은 행들을 묶어서 Order 1개 + OrderItem 여러 개로 변환
        orders: dict[str, models.Order] = {}
        for r in rows:
            order = orders.get(r.order_key)
            if order is None:
                order = models.Order(
                    customer=customers[r.business_number],
                    status='confirmed',
                    ordered_at=r.ordered_at
                )
                orders[r.order_key] = order
            order.items.append(
                models.OrderItem(product=products[r.sku], quantity=r.quantity, unit_price=r.unit_price)
            )

        import_repo.save_all(db, new_customers, new_products, list(orders.values()))

        return schemas.OrderImportResult(
            total_rows=len(rows),
            orders_created=len(orders),
            customers_created=len(new_customers),
            products_created=len(new_products)
        )

    def _parse_and_validate(self, content: bytes) -> list[ParsedRow]:
        """CSV 전체를 읽어서 list로 돌려준다."""
        # UTF-8이 아니면 400
        try:
            text = content.decode('utf-8-sig')
        except UnicodeDecodeError:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, 'UTF-8로 저장된 CSV 파일만 업로드할 수 있습니다.')

        # 빈 파일이면 400
        reader = csv.DictReader(io.StringIO(text))
        if not reader.fieldnames:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, '빈 파일입니다.')
        reader.fieldnames = [name.strip() for name in reader.fieldnames]

        # 필수 컬럼이 없으면 400
        missing = [c for c in REQUIRED_COLUMNS if c not in reader.fieldnames]
        if missing:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, f'필수 컬럼이 없습니다: {", ".join(missing)}')

        rows: list[ParsedRow] = []
        for line, raw in enumerate(reader, start=2):
            try:
                rows.append(self._parse_row(raw))
            except ValueError as e:
                raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f'{line}행: {e}')

        # 데이터가 없으면 400
        if not rows:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, '데이터 행이 없습니다.')
        
        return rows

    @staticmethod
    def _parse_row(raw: dict) -> ParsedRow:
        """한 행을 검증하고 ParsedRow로 변환"""
        def get(key: str) -> str:
            return (raw.get(key) or '').strip()

        order_key = get('order_id')
        business_number = get('business_number')
        company_name = get('company_name')
        sku = get('sku')
        product_name = get('product_name')

        if not order_key:
            raise ValueError('order_id가 비어 있습니다.')
        if not business_number or len(business_number) > 20:
            raise ValueError('business_number가 비었거나 20자를 넘습니다.')
        if not company_name:
            raise ValueError('company_name이 비어 있습니다.')        
        if not sku or len(sku) > 50:
            raise ValueError('sku가 비었거나 50자를 넘습니다.')
        if not product_name:
            raise ValueError('product_name이 비어 있습니다.')         

        try:
            ordered_at = datetime.fromisoformat(get("ordered_at"))
        except ValueError:
            raise ValueError('ordered_at 형식이 올바르지 않습니다. 예: 2026-01-01 12:30:00')
        if ordered_at.tzinfo is None:
            ordered_at = ordered_at.replace(tzinfo=timezone.utc)

        try:
            quantity = int(get('quantity'))
        except ValueError:
            raise ValueError('quantity는 정수여야 합니다.')
        if quantity <= 0:
            raise ValueError('quantity는 1 이상이어야 합니다.')

        try:
            unit_price = Decimal(get('unit_price'))
        except ValueError:
            raise ValueError('unit_price는 숫자여야 합니다.')
        if unit_price <= 0:
            raise ValueError('unit_price는 0보다 커야 합니다.')

        return ParsedRow(
            order_key=order_key,
            ordered_at=ordered_at,
            business_number=business_number,
            company_name=get('company_name'),
            sku=sku,
            product_name=get('product_name'),
            quantity=quantity,
            unit_price=unit_price
        )

import_service = ImportService()