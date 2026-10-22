import csv
import io
from datetime import date, datetime, timedelta, timezone

import pytest

from app.replenishment import daily_demand, days_until, make_plan, safety_stock


# ---------- 계산 함수 (DB 없이) ----------

WED = date(2026, 10, 7)          # 수요일. 이 주의 월요일은 10-05
MON = date(2026, 10, 5)


def flat_forecast(per_week=70.0, weeks=6):
    return {MON + timedelta(weeks=i): per_week for i in range(weeks)}


def test_daily_demand_counts_only_remaining_days_of_this_week():
    daily = daily_demand(flat_forecast(), WED)
    assert daily[0] == pytest.approx(10.0)        # 하루 수요 = 70 / 7
    assert len(daily) == 5 + 5 * 7                # 이번 주 수~일 5일 + 이후 5주


def test_days_until_exact_and_edges():
    daily = [10.0] * 20
    assert days_until(100, daily) == pytest.approx(10.0)
    assert days_until(0, daily) == 0.0             # 이미 바닥
    assert days_until(-5, daily) == 0.0
    assert days_until(10_000, daily) is None       # 예측 기간 안에 품절 없음


def test_safety_stock_grows_with_service_level_and_is_zero_without_error():
    assert safety_stock(0.0, 7, 0.95) == 0.0
    assert safety_stock(10.0, 7, 0.99) > safety_stock(10.0, 7, 0.90) > 0


def test_status_boundaries():
    daily = daily_demand(flat_forecast(), WED)     # 하루 10개, 리드타임 7일 → 리드타임 수요 70
    kwargs = dict(daily=daily, sigma_week=0.0, lead_days=7, cover_days=14)
    assert make_plan(stock=69, **kwargs).status == 'urgent'      # 리드타임 수요(70)보다 적음
    assert make_plan(stock=70, **kwargs).status == 'ok'          # 안전재고 0 이라 기준선 = 70
    plan = make_plan(stock=80, daily=daily, sigma_week=14.0, lead_days=7, cover_days=14)
    assert plan.status == 'order_now'                             # 70 <= 80 < 70 + 안전재고(약 23)


def test_recommended_qty():
    daily = daily_demand(flat_forecast(), WED)
    plan = make_plan(stock=100, daily=daily, sigma_week=0.0, lead_days=7, cover_days=14)
    assert plan.recommended_qty == 110             # 21일 * 10 - 재고 100
    assert make_plan(stock=1000, daily=daily, sigma_week=0.0, lead_days=7, cover_days=14).recommended_qty == 0


# ---------- API ----------

def build_csv(days=300):
    """P-A: 매일 주문(예측 대상) / P-B: 주문 3건뿐(예측 대상 아님)"""
    now = datetime.now(timezone.utc).replace(hour=10, minute=0, second=0, microsecond=0)
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(["order_id", "ordered_at", "business_number", "company_name", "sku", "product_name", "quantity", "unit_price"])
    for d in range(1, days + 1):
        ts = (now - timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([f"A{d}", ts, "123-45-67890", "테스트 제조", "P-A", "자주 팔리는 상품", 8 + d % 5, 1000])
    for d in (10, 100, 200):
        ts = (now - timedelta(days=d)).strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([f"B{d}", ts, "123-45-67890", "테스트 제조", "P-B", "드문 상품", 1, 5000])
    return out.getvalue().encode("utf-8")


def load_data(client, stock_a):
    response = client.post("/imports/orders", files={"file": ("orders.csv", build_csv(), "text/csv")})
    assert response.status_code == 201, response.text
    products = {p["sku"]: p for p in client.get("/products", params={"limit": 100}).json()}
    adjust = client.patch(f"/inventory/{products['P-A']['id']}", json={"amount": stock_a})
    assert adjust.status_code == 200
    return products


def test_replenishment_needs_enough_history(client):
    response = client.get("/replenishment")
    assert response.status_code == 409


def test_low_stock_is_urgent_and_unforecastable_product_uses_reorder_point(client):
    load_data(client, stock_a=5)
    response = client.get("/replenishment")
    assert response.status_code == 200
    body = response.json()
    assert body["lead_time_days"] == 7 and body["cover_days"] == 14

    items = {item["sku"]: item for item in body["items"]}
    a, b = items["P-A"], items["P-B"]

    assert a["method"] == "forecast"
    assert a["status"] == "urgent"
    assert a["recommended_qty"] > 0
    assert a["stockout_date"] is not None
    assert a["order_by_date"] == body["as_of"]            # 이미 발주 시점이 지남

    assert b["method"] == "reorder_point"
    assert b["status"] == "order_now"                     # 재고 0 <= reorder_point(10)
    assert b["recommended_qty"] is None

    assert body["items"][0]["status"] == "urgent"         # 급한 순으로 정렬


def test_plenty_of_stock_is_ok(client):
    load_data(client, stock_a=1_000_000)
    items = {item["sku"]: item for item in client.get("/replenishment").json()["items"]}
    assert items["P-A"]["status"] == "ok"
    assert items["P-A"]["stockout_date"] is None
    assert items["P-A"]["recommended_qty"] == 0


def test_needs_order_only_filters_ok_items(client):
    load_data(client, stock_a=1_000_000)
    body = client.get("/replenishment", params={"needs_order_only": True}).json()
    assert [item["sku"] for item in body["items"]] == ["P-B"]


def test_invalid_query_is_rejected(client):
    assert client.get("/replenishment", params={"lead_time_days": 100}).status_code == 422
