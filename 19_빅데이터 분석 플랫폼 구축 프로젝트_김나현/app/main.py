from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import Base, engine
from app.routers import customers, dashboard, inventory, orders, products, imports, forecasts, replenishment


@asynccontextmanager
async def lifespan(_: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="B2B Inventory Operations API",
    description="거래처 주문, 상품, 재고 및 운영 지표를 관리하는 B2B API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(products.router)
app.include_router(customers.router)
app.include_router(inventory.router)
app.include_router(orders.router)
app.include_router(dashboard.router)
app.include_router(imports.router)
app.include_router(forecasts.router)
app.include_router(replenishment.router)


@app.get("/health", tags=["system"])
def health_check():
    return {"status": "ok"}


# Jinja2 관리 화면
from app.web import install_web
install_web(app)
