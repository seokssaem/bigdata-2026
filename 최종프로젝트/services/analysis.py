"""
상품별 가격 집계 및 등락률 계산

- calc_change_vs_previous(): 직전 조사시점 대비 등락률/차액
- calc_change_vs_last_year(): 전년 동월 대비 등락률/차액 (가장 가까운 시점으로 매칭)
"""
import pandas as pd

from services.aggregation import aggregate_prices


def calc_change_vs_previous(agg: pd.DataFrame) -> pd.DataFrame:
    """상품별로 정렬된 시계열에서 바로 직전 조사시점 대비 등락률/차액을 계산."""
    out = agg.copy()
    out["이전가격"] = out.groupby("상품명")["평균가격"].shift(1)
    out["이전조사일"] = out.groupby("상품명")["조사일"].shift(1)
    out["차액"] = out["평균가격"] - out["이전가격"]
    out["등락률"] = ((out["평균가격"] - out["이전가격"]) / out["이전가격"] * 100).round(1)
    return out


def calc_change_vs_last_year(agg: pd.DataFrame, tolerance_days: int = 20) -> pd.DataFrame:
    """
    각 조사일에 대해, 정확히 1년 전과 가장 가까운 시점(±tolerance_days 이내)을
    찾아서 전년동기 등락률을 계산한다. 매칭되는 과거 시점이 없으면 결측으로 둔다.
    """
    results = []
    for product, g in agg.groupby("상품명"):
        g = g.sort_values("조사일").reset_index(drop=True)
        for i, row in g.iterrows():
            target = row["조사일"] - pd.DateOffset(years=1)
            diffs = (g["조사일"] - target).abs()
            within = diffs[diffs <= pd.Timedelta(days=tolerance_days)]
            if len(within) == 0:
                results.append({
                    "상품명": product, "조사일": row["조사일"],
                    "전년동기가격": None, "전년동기조사일": None,
                    "전년동기차액": None, "전년동기등락률": None,
                })
                continue
            match_idx = within.idxmin()
            base_price = g.loc[match_idx, "평균가격"]
            results.append({
                "상품명": product, "조사일": row["조사일"],
                "전년동기가격": base_price,
                "전년동기조사일": g.loc[match_idx, "조사일"],
                "전년동기차액": row["평균가격"] - base_price,
                "전년동기등락률": round((row["평균가격"] - base_price) / base_price * 100, 1),
            })
    return pd.DataFrame(results)


def build_full_analysis(raw_df: pd.DataFrame) -> pd.DataFrame:
    """원본(매장별) 데이터 → 등락률까지 다 계산된 최종 분석 테이블."""
    agg = aggregate_prices(raw_df)
    with_prev = calc_change_vs_previous(agg)
    with_yoy = calc_change_vs_last_year(agg)
    merged = with_prev.merge(with_yoy, on=["상품명", "조사일"], how="left")
    return merged


if __name__ == "__main__":
    raw_df = pd.read_pickle("data/prices_combined.pkl")
    result = build_full_analysis(raw_df)
    result.to_pickle("data/analysis_result.pkl")

    latest_date = result["조사일"].max()
    latest = result[result["조사일"] == latest_date].dropna(subset=["등락률"])

    print(f"등락률 계산 완료: {len(result)}행 (최신 조사일: {latest_date.date()})")
    print()
    print("=== 직전 대비 상승 TOP5 ===")
    print(latest.sort_values("등락률", ascending=False).head(5)
          [["상품명", "이전가격", "평균가격", "등락률"]].to_string(index=False))
