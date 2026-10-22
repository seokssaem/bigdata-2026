'''
발주 추천 서비스: 예측(forecast_service) + 현재 재고(inventory_repo) → 발주 계산(replenishment.py) → 응답 모양으로 정리

- 예측 대상 상품은 수요예측으로 예상 품절일과 추천 발주량을 계산한다.
- 예측 대상이 아닌 상품(주문이 드문 상품)은 기존 재주문 기준(reorder_point)으로만 판단한다.
'''
from datetime import date, datetime, timedelta, timezone
from math import ceil

import pandas as pd
from sqlalchemy.orm import Session

from app import schemas
from app.forecast_service import forecast_service
from app.replenishment import Plan, daily_demand, make_plan
from app.services import inventory_repo

MIN_HORIZON_WEEKS = 8   # 예상 품절일을 찾아볼 최소 예측 기간
STATUS_ORDER = {'urgent': 0, 'order_now': 1, 'ok': 2}


def _today() -> date:
    """주문 시각과 같은 기준(UTC)의 오늘 날짜"""
    return datetime.now(timezone.utc).date()


def _after(today: date, days: float | None) -> date | None:
    """오늘로부터 days일 뒤의 날짜 (None이면 None)"""
    return None if days is None else today + timedelta(days=int(days))


class ReplenishmentService:
    def overview(
        self,
        db: Session,
        lead_time_days: int,
        cover_days: int,
        service_level: float,
        needs_order_only: bool,
    ) -> schemas.ReplenishmentOverview:
        weeks = max(MIN_HORIZON_WEEKS, ceil((lead_time_days + cover_days) / 7) + 1)
        state, table = forecast_service.snapshot(db, weeks)
        today = _today()

        items = []
        for inv in inventory_repo.list(db, low_stock_only=False):
            if table is not None and inv.product_id in table.columns:
                items.append(self._forecast_item(inv, state, table, today, lead_time_days, cover_days, service_level))
            else:
                items.append(self._fallback_item(inv))

        if needs_order_only:
            items = [item for item in items if item.status != 'ok']

        # 급한 순서: 긴급 → 발주 필요 → 정상, 같은 상태에서는 품절이 빠른 순
        items.sort(key=lambda item: (STATUS_ORDER[item.status], item.stockout_date or date.max))

        return schemas.ReplenishmentOverview(
            as_of=today,
            lead_time_days=lead_time_days,
            cover_days=cover_days,
            service_level=service_level,
            horizon_weeks=weeks,
            items=items,
        )

    @staticmethod
    def _forecast_item(inv, state, table: pd.DataFrame, today: date, lead_time_days, cover_days, service_level):
        """수요예측 기반 계산"""
        pid = inv.product_id
        weekly_forecast = {week.date(): float(qty) for week, qty in table[pid].items()}
        daily = daily_demand(weekly_forecast, today)

        sigma = state.rmse.get(pid)
        sigma = 0.0 if sigma is None or pd.isna(sigma) else float(sigma)

        plan: Plan = make_plan(inv.quantity, daily, sigma, lead_time_days, cover_days, service_level)
        return schemas.ReplenishmentItem(
            product_id=pid,
            sku=inv.product.sku,
            name=inv.product.name,
            method='forecast',
            status=plan.status,
            current_stock=inv.quantity,
            stockout_date=_after(today, plan.stockout_in_days),
            order_by_date=_after(today, plan.order_by_in_days),
            recommended_qty=plan.recommended_qty,
            lead_time_demand=round(plan.lead_demand, 1),
            safety_stock=round(plan.safety_stock, 1),
            reorder_level=round(plan.reorder_level, 1),
        )

    @staticmethod
    def _fallback_item(inv):
        """예측 대상이 아닌 상품: 재주문 기준(reorder_point)으로만 판단"""
        needs = inv.quantity <= inv.product.reorder_point
        return schemas.ReplenishmentItem(
            product_id=inv.product_id,
            sku=inv.product.sku,
            name=inv.product.name,
            method='reorder_point',
            status='order_now' if needs else 'ok',
            current_stock=inv.quantity,
            stockout_date=None,
            order_by_date=None,
            recommended_qty=None,
            lead_time_demand=None,
            safety_stock=None,
            reorder_level=float(inv.product.reorder_point),
            note='예측 대상이 아니라 재주문 기준(reorder_point)으로 판단했습니다.',
        )


replenishment_service = ReplenishmentService()
