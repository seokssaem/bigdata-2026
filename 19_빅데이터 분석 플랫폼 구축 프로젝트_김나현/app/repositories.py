from collections.abc import Iterable, Iterator

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, selectinload

from app import models


class ProductRepository:
    def create(self, db: Session, product: models.Product, stock: int) -> models.Product:
        db.add(product)
        db.flush()
        db.add(models.Inventory(product_id=product.id, quantity=stock))
        db.commit()
        return self.get(db, product.id)

    def get(self, db: Session, product_id: int) -> models.Product | None:
        stmt = (
            select(models.Product)
            .options(selectinload(models.Product.inventory))
            .where(models.Product.id == product_id)
        )
        return db.scalar(stmt)

    def get_by_sku(self, db: Session, sku: str) -> models.Product | None:
        return db.scalar(select(models.Product).where(models.Product.sku == sku))

    def list(self, db: Session, search: str | None, skip: int, limit: int):
        stmt = select(models.Product).options(selectinload(models.Product.inventory))
        if search:
            pattern = f"%{search}%"
            stmt = stmt.where(or_(models.Product.sku.ilike(pattern), models.Product.name.ilike(pattern)))
        return list(db.scalars(stmt.offset(skip).limit(limit)).all())


class CustomerRepository:
    def create(self, db: Session, customer: models.Customer) -> models.Customer:
        db.add(customer)
        db.commit()
        db.refresh(customer)
        return customer

    def get(self, db: Session, customer_id: int) -> models.Customer | None:
        return db.get(models.Customer, customer_id)

    def get_by_business_number(self, db: Session, value: str) -> models.Customer | None:
        return db.scalar(select(models.Customer).where(models.Customer.business_number == value))

    def list(self, db: Session, skip: int, limit: int):
        return list(db.scalars(select(models.Customer).offset(skip).limit(limit)).all())


class InventoryRepository:
    def adjust(self, db: Session, inventory: models.Inventory, amount: int) -> models.Inventory:
        inventory.quantity += amount
        db.commit()
        db.refresh(inventory)
        return inventory

    def list(self, db: Session, low_stock_only: bool):
        stmt = select(models.Inventory).options(selectinload(models.Inventory.product))
        if low_stock_only:
            stmt = stmt.join(models.Product).where(models.Inventory.quantity <= models.Product.reorder_point)
        return list(db.scalars(stmt).all())


class OrderRepository:
    def create(self, db: Session, order: models.Order) -> models.Order:
        db.add(order)
        db.commit()
        return self.get(db, order.id)

    def get(self, db: Session, order_id: int) -> models.Order | None:
        stmt = (
            select(models.Order)
            .options(selectinload(models.Order.items))
            .where(models.Order.id == order_id)
        )
        return db.scalar(stmt)

    def list(self, db: Session, skip: int, limit: int):
        stmt = (
            select(models.Order)
            .options(selectinload(models.Order.items))
            .order_by(models.Order.ordered_at.desc())
            .offset(skip)
            .limit(limit)
        )
        return list(db.scalars(stmt).all())


class DashboardRepository:
    def summary(self, db: Session) -> dict:
        product_count = db.scalar(select(func.count(models.Product.id))) or 0
        customer_count = db.scalar(select(func.count(models.Customer.id))) or 0
        order_count = db.scalar(select(func.count(models.Order.id))) or 0
        total_sales = db.scalar(
            select(func.coalesce(func.sum(models.OrderItem.quantity * models.OrderItem.unit_price), 0))
        )
        low_stock_count = db.scalar(
            select(func.count(models.Inventory.id))
            .join(models.Product)
            .where(models.Inventory.quantity <= models.Product.reorder_point)
        ) or 0
        return {
            "product_count": product_count,
            "customer_count": customer_count,
            "order_count": order_count,
            "total_sales": total_sales,
            "low_stock_count": low_stock_count,
        }

def _chunks(values: list[str], size: int=500) -> Iterator[list[str]]:
    for i in range(0, len(values), size):
        yield values[i : i + size]

class ImportRepository:
    def get_customers_by_business_numbers(self, db: Session, business_numbers: Iterable[str]) -> dict[str, models.Customer]:
        """사업자번호 목록으로 기존 거래처를 찾아주는 함수"""
        found: dict[str, models.Customer] = {}
        for chunk in _chunks(list(business_numbers)):
            stmt = select(models.Customer).where(models.Customer.business_number.in_(chunk))
            for customer in db.scalars(stmt):
                found[customer.business_number] = customer
        return found

    def get_products_by_skus(self, db: Session, skus: Iterable[str]) -> dict[str, models.Product]:
        """sku 목록으로 기존 상품을 찾아주는 함수"""
        found: dict[str, models.Product] = {}
        for chunk in _chunks(list(skus)):
            stmt = select(models.Product).where(models.Product.sku.in_(chunk))
            for product in db.scalars(stmt):
                found[product.sku] = product
        return found

    def save_all(
        self,
        db: Session,
        customers: list[models.Customer],
        products: list[models.Product],
        orders: list[models.Order]
    ) -> None:
        """새 거래처/상품/주문을 한 트랜잭션으로 저장 (하나라도 실패하면 전부 롤백)"""
        try:
            db.add_all(customers)
            db.add_all(products)
            db.add_all(orders)
            db.commit()
        except Exception:
            db.rollback()
            raise

class ForecastRepository:
    def order_lines(self, db: Session) -> list[tuple]:
        """확정 주문의 (상품 id, 주문 시각, 수량) 행을 전부 가져온다."""
        stmt = (
            select(models.OrderItem.product_id, models.Order.ordered_at, models.OrderItem.quantity)
            .join(models.Order, models.Order.id == models.OrderItem.order_id)
            .where(models.Order.status == 'confirmed')
        )
        return [tuple(row) for row in db.execute(stmt).all()]