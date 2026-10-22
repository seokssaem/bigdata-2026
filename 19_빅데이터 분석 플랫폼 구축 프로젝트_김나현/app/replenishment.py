"""추천 발주량·예상 품절일 계산 (DB, FastAPI를 모르는 순수 계산 코드)"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from math import ceil, sqrt
from statistics import NormalDist


def daily_demand(weekly_forecast: dict[date, float], today: date) -> list[float]:
    """주간 예측({월요일: 수량})을 오늘부터 하루씩의 예상 수요로 펼친다.
    이번 주는 오늘 이후 남은 날만 담기므로, 이미 재고에서 빠진 지난 날은 세지 않는다."""
    last_day = max(weekly_forecast) + timedelta(days=6)
    out, d = [], today
    while d <= last_day:
        monday = d - timedelta(days=d.weekday())
        out.append(weekly_forecast.get(monday, 0.0) / 7)
        d += timedelta(days=1)
    return out


def days_until(drop: float, daily: list[float]) -> float | None:
    """누적 수요가 drop만큼 쌓이는 때까지 걸리는 일수(오늘 0시 기준, 소수 가능).
    이미 drop 이하면 0, 예측 기간 안에 도달하지 않으면 None."""
    if drop <= 0:
        return 0.0
    cum = 0.0
    for i, x in enumerate(daily):
        if x > 0 and cum + x >= drop:
            return i + (drop - cum) / x
        cum += x
    return None


def safety_stock(sigma_week: float, lead_days: int, service_level: float) -> float:
    z = NormalDist().inv_cdf(service_level)
    return z * sigma_week * sqrt(lead_days / 7)


@dataclass(frozen=True)
class Plan:
    status: str                      # 'urgent' | 'order_now' | 'ok'
    stockout_in_days: float | None
    order_by_in_days: float | None
    lead_demand: float
    safety_stock: float
    reorder_level: float
    recommended_qty: int


def make_plan(stock: int, daily: list[float], sigma_week: float,
              lead_days: int, cover_days: int, service_level: float = 0.95) -> Plan:
    lead_demand = sum(daily[:lead_days])
    ss = safety_stock(sigma_week, lead_days, service_level)
    level = lead_demand + ss                              # 이 밑으로 내려가면 발주
    target = sum(daily[:lead_days + cover_days]) + ss
    status = 'urgent' if stock < lead_demand else 'order_now' if stock < level else 'ok'
    return Plan(
        status=status,
        stockout_in_days=days_until(stock, daily),
        order_by_in_days=days_until(stock - level, daily),
        lead_demand=lead_demand,
        safety_stock=ss,
        reorder_level=level,
        recommended_qty=max(0, ceil(target - stock)),
    )
