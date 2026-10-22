from datetime import datetime, date
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    unit_price: Decimal = Field(gt=0)
    reorder_point: int = Field(default=10, ge=0)
    initial_stock: int = Field(default=0, ge=0)


class ProductRead(ORMModel):
    id: int
    sku: str
    name: str
    unit_price: Decimal
    reorder_point: int
    stock_quantity: int


class CustomerCreate(BaseModel):
    company_name: str = Field(min_length=1, max_length=200)
    business_number: str = Field(min_length=1, max_length=20)
    contact_name: str | None = None
    contact_email: str | None = None


class CustomerRead(ORMModel):
    id: int
    company_name: str
    business_number: str
    contact_name: str | None
    contact_email: str | None


class StockAdjustment(BaseModel):
    amount: int


class InventoryRead(BaseModel):
    product_id: int
    sku: str
    name: str
    quantity: int
    reorder_point: int
    needs_reorder: bool


class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class OrderCreate(BaseModel):
    customer_id: int
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(ORMModel):
    product_id: int
    quantity: int
    unit_price: Decimal


class OrderRead(ORMModel):
    id: int
    customer_id: int
    status: str
    ordered_at: datetime
    items: list[OrderItemRead]
    total_amount: Decimal


class DashboardSummary(BaseModel):
    product_count: int
    customer_count: int
    order_count: int
    total_sales: Decimal
    low_stock_count: int

class OrderImportResult(BaseModel):
    total_rows: int
    orders_created: int
    products_created: int
    customers_created: int

class WeeklyPoint(BaseModel):
    week_start: date
    quantity: float

class ProductForecast(BaseModel):
    product_id: int
    sku: str
    name: str
    model: str
    backtest_wape: float | None
    active_week_ratio: float
    history: list[WeeklyPoint]
    forecast: list[WeeklyPoint]

class ExcludedProduct(BaseModel):
    product_id: int
    sku: str
    name: str
    active_week_ratio: float
    reason: str

class ForecastOverview(BaseModel):
    weeks: int
    min_active_week_ratio: float
    forecasts: list[ProductForecast]
    excluded: list[ExcludedProduct]

class ReplenishmentItem(BaseModel):
    product_id: int
    sku: str
    name: str
    method: str                        # 'forecast'(수요예측 기반) | 'reorder_point'(예측 대상이 아니라 재주문 기준으로 판단)
    status: str                        # 'urgent'(리드타임 안에 품절 예상) | 'order_now'(지금 발주) | 'ok'
    current_stock: int
    stockout_date: date | None         # 예상 품절일. None이면 예측 기간 안에 품절되지 않음(또는 계산 불가)
    order_by_date: date | None         # 늦어도 이 날까지는 발주해야 하는 날짜
    recommended_qty: int | None        # 추천 발주량. 예측 대상이 아니면 None
    lead_time_demand: float | None     # 리드타임 동안 예상 수요
    safety_stock: float | None
    reorder_level: float | None        # 이 재고 밑으로 내려가면 발주 (리드타임 수요 + 안전재고)
    note: str | None = None

class ReplenishmentOverview(BaseModel):
    as_of: date
    lead_time_days: int
    cover_days: int
    service_level: float
    horizon_weeks: int
    items: list[ReplenishmentItem]
