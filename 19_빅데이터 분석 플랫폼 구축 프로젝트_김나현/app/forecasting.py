'''
주간 수요 예측 로직

주문 데이터 표를 넣으면 예측 숫자가 나오는 "계산 담당" 파일
'''
from __future__ import annotations

from datetime import datetime

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor

LAGS = 4    # 최근 몇 주를 보고 다음 주를 예측할지
FEATURE_COLS = ["lag_1", "lag_2", "lag_3", "lag_4", "avg_4", "month_start_days"]
ACTIVE_WINDOW_WEEKS = 52    # "상품별 주문 있던 주 비율"을 계산할 기간 (1년)

def _monday_of(ts: pd.Series) -> pd.Series:
    """각 시각이 속한 주의 월요일 00:00"""
    day = ts.dt.normalize()
    return day - pd.to_timedelta(day.dt.weekday, unit='D')

def weekly_sales(lines: pd.DataFrame, now: datetime) -> pd.DataFrame:
    """
    주문 행(product_id, ordered_at, quantity)을 '주 x 상품' 수량 표로 바꾼다.

    - 주는 월~일 기준, 인덱스는 그 주의 월요일
    - 주문이 없던 주는 0으로 채운다.
    - 데이터가 주 중간에 시작하면 첫 주도 뺀다.
    - 아직 끝나지 않은 이번주는 뺀다.
    """
    if lines.empty:
        return pd.DataFrame()

    df = lines.copy()
    # DB마다 다른 타임존 포맷을 통일
    df['ordered_at'] = pd.to_datetime(df['ordered_at'], utc=True).dt.tz_localize(None)
    df['week_start'] = _monday_of(df['ordered_at'])

    weekly = df.pivot_table(
        index='week_start', columns='product_id', values='quantity', aggfunc='sum', fill_value=0
    )

    first_week = weekly.index.min()
    if df['ordered_at'].min().normalize() != first_week:
        first_week += pd.Timedelta(weeks=1)
    last_week = _monday_of(pd.Series([now])).iloc[0] - pd.Timedelta(weeks=1)
    full_weeks = pd.date_range(first_week, last_week, freq='7D')    

    weekly = weekly.reindex(full_weeks, fill_value=0).astype(float) # 주문 없었던 주 포함
    weekly.index.name = 'week_start'
    weekly.columns.name = None

    return weekly

def active_week_ratio(weekly: pd.DataFrame, window: int = ACTIVE_WINDOW_WEEKS) -> pd.Series:
    """상품별로 최근 window주 중 주문이 있었던 주의 비율 (0~1)"""
    return (weekly.tail(window) > 0).mean()

def month_start_days(week_start: pd.Timestamp) -> int:
    """그 주(월~일)에 '매월 1~7일'이 며칠 들어 있는지 (0~7). 월초 정기 발주 효과용"""
    return sum((week_start + pd.Timedelta(days=i)).day <= 7 for i in range(7))

def build_table(weekly: pd.DataFrame) -> pd.DataFrame:
    """
    학습/평가용 표
    
    lag_1 ~ lag_LAGS: 1~LAGS주 전 수량
    target: 그 주 수량
    """
    lag_cols = [f'lag_{i}' for i in range(1, LAGS+1)]
    tables = []

    for pid in weekly.columns:
        sales = weekly[pid]
        table = pd.DataFrame({
            'product_id':pid,
            'week_start':sales.index,
            'target':sales.values
        })

        for i, col in enumerate(lag_cols, start=1):
            table[col] = sales.shift(i).values

        table[f'avg_{LAGS}'] = table[lag_cols].mean(axis=1)
        table['month_start_days'] = [month_start_days(week) for week in table['week_start']]

        tables.append(table.iloc[LAGS:])    # 앞쪽 4주는 lag가 없어서 버림

    return pd.concat(tables, ignore_index=True)

def wape(actual, pred) -> float:
    """
    WAPE = |오차| 합 / 실제 판매량 합.
    ex) 0.2 → '전체 판매량의 20% 정도 틀림'.
    """
    actual = np.asarray(actual, dtype=float)
    total = actual.sum()
    return float(np.abs(actual - np.asarray(pred, dtype=float)).sum() / total) if total > 0 else float('nan')

MIN_ACTIVE_WEEK_RATIO = 0.8
HOLDOUT_WEEKS = 8   
MIN_HISTORY_WEEKS = 26      # 이보다 주간 데이터가 짧으면 예측하지 않음
RF_PARAMS = dict(n_estimators=200, min_samples_leaf=2, random_state=42, n_jobs=1)

def split_eligible(weekly: pd.DataFrame, min_ratio: float=MIN_ACTIVE_WEEK_RATIO):
    """(예측 대상 상품 id 목록, 상품별 비율)"""
    ratio = active_week_ratio(weekly)
    return list(ratio[ratio >= min_ratio].index), ratio

def feature_row(product_id, history: list[float], week_start: pd.Timestamp) -> dict:
    """
    예측할 때 쓰는 입력값 한 줄
    build_table의 컬럼들과 의미가 같아야 한다.

    - history: 그 주 직전까지의 주간 수량 리스트
    """
    row = {'product_id': product_id, 'week_start': week_start}
    
    for k in range(1, LAGS + 1):
        row[f'lag_{k}'] = history[-k]
    row['avg_4'] = float(np.mean(history[-LAGS:]))
    row['month_start_days'] = month_start_days(week_start)
    return row

class DemandForecaster:
    """상품마다 랜덤포레스트를 따로 학습한다."""

    name = 'random_forest_per_product'

    def fit(self, weekly: pd.DataFrame) -> "DemandForecaster":
        table = build_table(weekly)
        self.models_ = {
            # {상품 id: 그 상품 전용 모델}
            product_id: RandomForestRegressor(**RF_PARAMS).fit(product_rows[FEATURE_COLS], product_rows['target'])
            for product_id, product_rows in table.groupby('product_id')
        }
        return self

    def predict_rows(self, rows: pd.DataFrame) -> np.ndarray:
        """rows의 예측값. 줄마다 그 상품의 모델로 예측한다."""
        rows = rows.reset_index(drop=True)
        pred = np.zeros(len(rows))  # 초기화
        for product_id in rows['product_id'].unique():
            is_this_product = (rows['product_id'] == product_id).to_numpy()
            pred[is_this_product] = self.models_[product_id].predict(rows.loc[is_this_product, FEATURE_COLS])
        return np.clip(pred, 0, None)   # 음수를 0으로 제한

    def forecast(self, weekly: pd.DataFrame, horizon: int) -> pd.DataFrame:
        """
        다음 horizon주를 예측한다. (index=예측 주 월요일, columns=상품 id)
            - 한 주씩 예측하고, 그 예측값을 다음 주의 lag로 넣어서 이어간다.
            - 먼 주일수록 정확도는 떨어진다.
        """
        histories = {product_id: weekly[product_id].tolist() for product_id in weekly.columns}
        out = {}
        for step in range(1, horizon + 1):
            week = weekly.index[-1] + pd.Timedelta(weeks=step)
            rows = pd.DataFrame(
                [feature_row(product_id, history, week) for product_id, history in histories.items()]
            )
            preds = self.predict_rows(rows)

            for product_id, pred in zip(histories, preds):
                histories[product_id].append(float(pred))

            out[week] = dict(zip(histories, preds))

        return pd.DataFrame(out).T

def backtest_errors(weekly: pd.DataFrame, holdout_weeks: int=HOLDOUT_WEEKS) -> pd.DataFrame:
    """
    상품별 '다음 1주' 예측 오차.
    마지막 holdout_weeks주를 학습에서 빼고 맞혀본다.

    열: wape (비율, 0.2 = 20% 틀림), rmse (주간 수량 단위 오차, 안전재고 계산에 사용)
    """
    forecaster = DemandForecaster().fit(weekly.iloc[:-holdout_weeks])
    table = build_table(weekly)
    test = table[table['week_start'] >= weekly.index[-holdout_weeks]].copy()
    test['pred'] = forecaster.predict_rows(test)

    rows = {}
    for pid, g in test.groupby('product_id'):
        err = g['target'].to_numpy(dtype=float) - g['pred'].to_numpy(dtype=float)
        rows[pid] = {'wape': wape(g['target'], g['pred']), 'rmse': float(np.sqrt(np.mean(err ** 2)))}
    return pd.DataFrame.from_dict(rows, orient='index')

def backtest_wape(weekly: pd.DataFrame, holdout_weeks: int=HOLDOUT_WEEKS) -> pd.Series:
    """상품별 백테스트 WAPE만 필요할 때 (노트북 등 기존 코드 호환용)"""
    return backtest_errors(weekly, holdout_weeks)['wape']
