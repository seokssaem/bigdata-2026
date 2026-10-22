'''
예측 서비스: DB에서 주문을 꺼내(repository) → 예측 계산(forecasting.py) → 응답 모양으로 정리
모델 학습은 데이터가 바뀌었을 때만 다시 한다.
'''
import threading
from dataclasses import dataclass, field
from datetime import datetime, timezone

import pandas as pd
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app import schemas
from app.forecasting import (
    ACTIVE_WINDOW_WEEKS,
    MIN_ACTIVE_WEEK_RATIO,
    MIN_HISTORY_WEEKS,
    DemandForecaster,
    backtest_errors,
    split_eligible,
    weekly_sales,
)
from app.repositories import ForecastRepository
from app.services import product_repo

forecast_repo = ForecastRepository()

def _now() -> datetime:
    """주문 시각(ordered_at)과 같은 기준(naive UTC)의 현재 시각"""
    return datetime.now(timezone.utc).replace(tzinfo=None)

@dataclass
class _State:
    """학습이 끝난 결과 묶음"""
    signature: tuple
    weekly: pd.DataFrame            # 전체 상품의 주간 수량
    ratio: pd.Series                # 상품별 '주문 있던 주' 비율
    eligible: list                  # 예측 대상 상품 id
    forecaster: object              # 학습 끝난 모델 (예측 대상이 없으면 None)
    wape: pd.Series                 # 상품별 백테스트 WAPE
    rmse: pd.Series                 # 상품별 백테스트 RMSE (주간 수량 단위, 안전재고 계산용)
    forecasts: dict = field(default_factory=dict)   # {weeks: 예측 표} 캐시

class ForecastService:
    def __init__(self):
        self._lock = threading.Lock()   # 동시성 제어
        self._state: _State | None = None

    def _prepare(self, db: Session) -> _State:
        """
        DB 주문을 주간 표로 바꾸고, 
        데이터가 바뀐 경우에만 대상 선정, 백테스트, 모델 학습을 다시 해서 결과 묶음을 돌려준다.
        """
        lines = pd.DataFrame(
            forecast_repo.order_lines(db),
            columns=['product_id', 'ordered_at', 'quantity']
        )
        weekly = weekly_sales(lines, _now())
        if weekly.shape[0] < MIN_HISTORY_WEEKS:
            raise HTTPException(
                status.HTTP_409_CONFLICT,
                f'예측에는 주간 데이터가 {MIN_HISTORY_WEEKS}주 이상 필요합니다. (현재 {weekly.shape[0]}주)'
            )

        signature = (weekly.shape, weekly.index[-1], float(weekly.to_numpy().sum()))
        with self._lock:
            if self._state is not None and self._state.signature == signature:
                return self._state

            eligible, ratio = split_eligible(weekly)
            forecaster = None
            wape = rmse = pd.Series(dtype=float)
            if eligible:
                weekly_eligible = weekly[eligible]
                errors = backtest_errors(weekly_eligible)
                wape, rmse = errors['wape'], errors['rmse']
                forecaster = DemandForecaster().fit(weekly_eligible)

            self._state = _State(signature, weekly, ratio, eligible, forecaster, wape, rmse)
            return self._state

    def snapshot(self, db: Session, weeks: int) -> tuple[_State, pd.DataFrame | None]:
        """다른 서비스(발주 추천 등)가 쓰는 공개 메서드: (학습 결과, 다음 weeks주 예측 표).
        예측 대상 상품이 하나도 없으면 예측 표는 None."""
        state = self._prepare(db)
        table = self._forecast_table(state, weeks) if state.eligible else None
        return state, table

    @staticmethod
    def _forecast_table(state: _State, weeks: int) -> pd.DataFrame:
        """예측 대상 전체 상품의 다음 weeks주 예측 표를 돌려준다."""
        if weeks not in state.forecasts:
            state.forecasts[weeks] = state.forecaster.forecast(state.weekly[state.eligible], weeks)
        return state.forecasts[weeks]

    @staticmethod
    def _points(series: pd.Series, digits: int | None=None) -> list[schemas.WeeklyPoint]:
        """
        주 날짜가 인덱스인 Series를 [{week_start, quantity}, ...] 응답 목록으로 바꾼다. 
        (digits가 있으면 그 자리까지 반올림)
        """
        return [
            schemas.WeeklyPoint(week_start=week.date(), quantity=round(float(v), digits) if digits is not None else float(v))
            for week, v in series.items()
        ]

    def _build_forecast(self, state: _State, product, weeks: int, history_weeks: int) -> schemas.ProductForecast:
        """상품 하나의 응답(상품 정보, 백테스트 WAPE, 최근 실적, 예측)을 만든다."""
        pid = product.id
        wape = state.wape.get(pid)
        return schemas.ProductForecast(
            product_id=pid,
            sku=product.sku,
            name=product.name,
            model=state.forecaster.name,
            backtest_wape=None if wape is None or pd.isna(wape) else round(float(wape), 3),
            active_week_ratio=round(float(state.ratio[pid]), 3),
            history=self._points(state.weekly[pid].tail(history_weeks)) if history_weeks else [],
            forecast=self._points(self._forecast_table(state, weeks)[pid], digits=1)
        )

    @staticmethod
    def _exclusion_reason(ratio: float) -> str:
        """예측 대상에서 제외된 이유를 사용자에게 보여줄 문장으로 만든다."""
        return (
            f"최근 {ACTIVE_WINDOW_WEEKS}주 중 주문이 있었던 주가 {ratio:.0%}라서 예측 대상이 아닙니다. "
            f"(기준: {MIN_ACTIVE_WEEK_RATIO:.0%} 이상)"
        )

    def for_product(self, db: Session, product_id: int, weeks: int, history_weeks: int) -> schemas.ProductForecast:
        """
        상품 하나의 예측을 돌려준다. 
        (없으면 404, 대상이 아니면 422)
        """
        product = product_repo.get(db, product_id)
        if not product:
            raise HTTPException(status.HTTP_404_NOT_FOUND, '상품을 찾을 수 없습니다.')

        state = self._prepare(db)
        if product_id not in state.eligible:
            ratio = float(state.ratio.get(product_id, 0.0))
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, self._exclusion_reason(ratio))
        return self._build_forecast(state, product, weeks, history_weeks)

    def overview(self, db: Session, weeks: int, history_weeks: int) -> schemas.ForecastOverview:
        """전체 상품을 예측 대상(forecasts)과 제외 상품(excluded)으로 나눠서 한 번에 돌려준다."""
        state = self._prepare(db)
        forecasts, excluded = [], []
        for product in product_repo.list(db, None, 0, 100000):
            if product.id in state.eligible:
                forecasts.append(self._build_forecast(state, product, weeks, history_weeks))
            else:
                ratio = float(state.ratio.get(product.id, 0.0))
                excluded.append(
                    schemas.ExcludedProduct(
                        product_id=product.id,
                        sku=product.sku,
                        name=product.name,
                        active_week_ratio=round(ratio, 3),
                        reason=self._exclusion_reason(ratio)                    
                    )
                )

        return schemas.ForecastOverview(
            weeks=weeks,
            min_active_week_ratio=MIN_ACTIVE_WEEK_RATIO,
            forecasts=forecasts,
            excluded=excluded
        )

forecast_service = ForecastService()