from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.repositories import (
    CustomerRepository,
    DashboardRepository,
    InventoryRepository,
    OrderRepository,
    ProductRepository,
)


product_repo = ProductRepository()
customer_repo = CustomerRepository()
inventory_repo = InventoryRepository()
order_repo = OrderRepository()
dashboard_repo = DashboardRepository()


class ProductService:
    def create(self, db: Session, data: schemas.ProductCreate):
        if product_repo.get_by_sku(db, data.sku):
            raise HTTPException(status_code=409, detail="이미 등록된 SKU입니다.")
        product = models.Product(
            sku=data.sku,
            name=data.name,
            unit_price=data.unit_price,
            reorder_point=data.reorder_point,
        )
        return product_repo.create(db, product, data.initial_stock)

    def list(self, db: Session, search: str | None, skip: int, limit: int):
        return product_repo.list(db, search, skip, limit)

    @staticmethod
    def to_read(product: models.Product) -> schemas.ProductRead:
        return schemas.ProductRead(
            id=product.id,
            sku=product.sku,
            name=product.name,
            unit_price=product.unit_price,
            reorder_point=product.reorder_point,
            stock_quantity=product.inventory.quantity,
        )


class CustomerService:
    def create(self, db: Session, data: schemas.CustomerCreate):
        if customer_repo.get_by_business_number(db, data.business_number):
            raise HTTPException(status_code=409, detail="이미 등록된 사업자번호입니다.")
        return customer_repo.create(db, models.Customer(**data.model_dump()))


class InventoryService:
    def adjust(self, db: Session, product_id: int, amount: int):
        product = product_repo.get(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="상품을 찾을 수 없습니다.")
        if product.inventory.quantity + amount < 0:
            raise HTTPException(status_code=400, detail="재고는 0보다 작을 수 없습니다.")
        return inventory_repo.adjust(db, product.inventory, amount)


class OrderService:
    def create(self, db: Session, data: schemas.OrderCreate):
        if not customer_repo.get(db, data.customer_id):
            raise HTTPException(status_code=404, detail="거래처를 찾을 수 없습니다.")

        requested: dict[int, int] = {}
        for item in data.items:
            requested[item.product_id] = requested.get(item.product_id, 0) + item.quantity

        products: dict[int, models.Product] = {}
        for product_id, quantity in requested.items():
            product = product_repo.get(db, product_id)
            if not product:
                raise HTTPException(status_code=404, detail=f"상품 {product_id}를 찾을 수 없습니다.")
            if product.inventory.quantity < quantity:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"{product.sku}의 재고가 부족합니다.",
                )
            products[product_id] = product

        order = models.Order(customer_id=data.customer_id)
        for product_id, quantity in requested.items():
            product = products[product_id]
            product.inventory.quantity -= quantity
            order.items.append(
                models.OrderItem(
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=product.unit_price,
                )
            )
        return order_repo.create(db, order)

    @staticmethod
    def to_read(order: models.Order) -> schemas.OrderRead:
        total = sum((item.unit_price * item.quantity for item in order.items), Decimal("0"))
        return schemas.OrderRead(
            id=order.id,
            customer_id=order.customer_id,
            status=order.status,
            ordered_at=order.ordered_at,
            items=order.items,
            total_amount=total,
        )


product_service = ProductService()
customer_service = CustomerService()
inventory_service = InventoryService()
order_service = OrderService()

