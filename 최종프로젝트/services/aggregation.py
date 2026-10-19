"""
매장별 개별 가격 데이터를 상품×조사일 평균가격으로 집계하는 공통 함수.

analysis.py, load_to_db.py, predictor.py가 각자 따로 집계 로직을 갖고 있었는데,
여기 하나로 합쳐서 모든 곳에서 같은 기준(표본 수 필터 포함)을 쓰도록 했다.

표본 필터는 "그 상품의 평소 매장 수 대비 비율"(상대기준)로만 건다:
- 평소 180개 매장에서 조사되던 상품이 어느 시점에 18개로 뚝 떨어지면(평소의 10%),
  그 시점 평균은 표본이 달라져서 생긴 노이즈라 제외한다.
- "매장 20개 미만이면 무조건 제외" 같은 절대기준은 쓰지 않는다. 갈치, 깻잎, 오징어처럼
  원래 4~13개 매장에서만 조사되는 신선식품이 통째로(30개 상품) 사라지기 때문이다.
  그런 상품은 매번 비슷한 규모로 조사되므로 평균을 비교해도 노이즈가 아니다.
"""
import pandas as pd


def aggregate_prices(
    raw_df: pd.DataFrame,
    min_ratio_vs_median: float = 0.3,
) -> pd.DataFrame:
    """
    raw_df: 상품명, 조사일, 판매가격 컬럼이 있는 매장별 원본 데이터
    반환: 상품명, 조사일, 평균가격, 매장수 컬럼
          (그 상품 평소 매장수 대비 min_ratio_vs_median 미만인 조사시점은 제외)
    """
    grouped = raw_df.groupby(["상품명", "조사일"])["판매가격"].agg(["mean", "count"]).reset_index()
    grouped = grouped.rename(columns={"mean": "평균가격", "count": "매장수"})
    grouped["평균가격"] = grouped["평균가격"].round(0)
    grouped["조사일"] = pd.to_datetime(grouped["조사일"])

    # 상품별 평소(중앙값) 매장수 계산 → 그 상품 기준으로 "표본이 평소보다 확 줄었는지" 판단
    median_stores = grouped.groupby("상품명")["매장수"].transform("median")

    before = len(grouped)
    keep = grouped["매장수"] >= median_stores * min_ratio_vs_median
    grouped = grouped[keep].reset_index(drop=True)
    removed = before - len(grouped)
    if removed > 0:
        print(f"[aggregate_prices] 평소 매장 수 대비 {min_ratio_vs_median*100:.0f}% 미만인 "
              f"조사시점 제외: {removed}개")

    return grouped.sort_values(["상품명", "조사일"]).reset_index(drop=True)
