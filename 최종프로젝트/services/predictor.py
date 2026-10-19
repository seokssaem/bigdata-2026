"""
상품별 가격 예측 (선형회귀)

상품마다 지금까지의 조사 시점을 순서대로 1,2,3...으로 두고(X),
그때의 평균가격(y)으로 LinearRegression을 학습시켜서
다음 조사 시점의 예상 가격을 계산한다.

너무 적은 시점(min_points 미만)만 있는 상품은 예측 신뢰도가 낮아서 건너뛴다.
"""
import pandas as pd
from sklearn.linear_model import LinearRegression
import numpy as np

from services.aggregation import aggregate_prices


def predict_next_price(
    price_series: pd.DataFrame,
    min_points: int = 6,
    recent_window: int = 10,
    max_change_rate: float = 15.0,
) -> dict | None:
    """
    한 상품의 (조사일, 평균가격) 시계열을 받아서 다음 시점 예측가를 반환.
    price_series: '조사일'(datetime), '평균가격' 컬럼을 가진 DataFrame (해당 상품만)

    - recent_window: 전체 기간 대신 최근 N개 시점만 사용해서 학습
      (옛날 추세나 한 번성 급등락에 모델이 과하게 휘둘리지 않도록)
    - max_change_rate: 예측 등락률의 상한/하한(%). 이 범위를 넘으면 잘라낸다
      (선형회귀가 극단적으로 튀는 값을 뱉는 걸 마지막에 한 번 더 막는 안전장치)

    반환: {"예측가격": ..., "기준가격": ..., "예상등락률": ...} 또는 None(데이터 부족시)
    """
    g = price_series.sort_values("조사일").reset_index(drop=True)
    if len(g) < min_points:
        return None

    # 최근 recent_window개 시점만 사용
    g = g.tail(recent_window).reset_index(drop=True)

    X = np.arange(len(g)).reshape(-1, 1)
    y = g["평균가격"].values

    model = LinearRegression()
    model.fit(X, y)

    next_x = np.array([[len(g)]])
    predicted = model.predict(next_x)[0]

    current_price = g["평균가격"].iloc[-1]
    change_rate = (predicted - current_price) / current_price * 100

    # 변동폭 상한/하한 적용 (너무 극단적인 예측값 완화)
    clipped_rate = max(-max_change_rate, min(max_change_rate, change_rate))
    clipped_price = current_price * (1 + clipped_rate / 100)

    return {
        "예측가격": round(clipped_price),
        "기준가격": current_price,
        "예상등락률": round(clipped_rate, 1),
        "원본예측등락률": round(change_rate, 1),  # 상한 적용 전 원래 값 (참고용)
    }


def predict_all_products(agg_df: pd.DataFrame, min_points: int = 6) -> pd.DataFrame:
    """
    상품×조사일 평균가격 테이블(agg_df) 전체를 받아서,
    상품마다 다음 시점 예측 결과를 한 행씩 담은 DataFrame을 반환한다.
    """
    results = []
    for product, g in agg_df.groupby("상품명"):
        pred = predict_next_price(g[["조사일", "평균가격"]], min_points=min_points)
        if pred is None:
            continue
        results.append({
            "상품명": product,
            "기준가격": pred["기준가격"],
            "예측가격": pred["예측가격"],
            "예상등락률": pred["예상등락률"],
            "원본예측등락률": pred["원본예측등락률"],
        })
    return pd.DataFrame(results)


if __name__ == "__main__":
    raw = pd.read_pickle("data/prices_combined.pkl")
    agg = aggregate_prices(raw)

    predictions = predict_all_products(agg)
    predictions.to_csv("data/price_predictions.csv", index=False, encoding="utf-8-sig")

    print(f"예측 완료: {len(predictions)}개 상품")
    print()
    print("=== 다음에 오를 것 같은 상품 TOP5 (예상 상승률 순) ===")
    print(predictions.sort_values("예상등락률", ascending=False).head(5)
          [["상품명", "기준가격", "예측가격", "예상등락률", "원본예측등락률"]].to_string(index=False))
    print()
    print("=== 다음에 내릴 것 같은 상품 TOP5 (예상 하락률 순) ===")
    print(predictions.sort_values("예상등락률").head(5)
          [["상품명", "기준가격", "예측가격", "예상등락률", "원본예측등락률"]].to_string(index=False))
    print()
    clipped = predictions[predictions["예상등락률"] != predictions["원본예측등락률"]]
    print(f"상한/하한에 걸려서 값이 조정된 상품: {len(clipped)}개 / {len(predictions)}개")
