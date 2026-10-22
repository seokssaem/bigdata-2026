'''
더미 주문 CSV 생성기 (수요 예측 테스트용) - 제조/산업 부품

사용 예
- python dummy_orders.py --days 365 --seed 42 --out data/dummy_orders.csv

상품마다 '심어둔 패턴'(추세, 프로젝트성 수요 급증)이 있어서
나중에 예측 모델이 이 패턴을 잘 찾는지 검증할 수 있다.
같은 seed면 항상 같은 CSV가 나온다.
'''
import argparse
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

@dataclass(frozen=True)
class ProductSpec:
    sku: str
    name: str
    price: str
    popularity: float   # 클수록 자주 팔림
    typical_qty: int    # 한 주문 라인당 평균 수량
    trend: float        # 기간 전체에 걸친 증감률

PRODUCTS = [
    ProductSpec("P-001", "산업용 센서", 45000, 5.0, 20, 0.15),
    ProductSpec("P-002", "근접 스위치", 28000, 4.0, 25, 0.00),
    ProductSpec("P-003", "M12 커넥터", 8500, 5.0, 60, 0.05),
    ProductSpec("P-004", "케이블 하네스", 15000, 3.5, 40, -0.10),
    ProductSpec("P-005", "PLC 모듈", 380000, 0.8, 3, 0.20),
    ProductSpec("P-006", "서보 모터", 520000, 0.5, 2, 0.10),
    ProductSpec("P-007", "모터 드라이버", 210000, 0.7, 3, 0.10),
    ProductSpec("P-008", "DIN 레일 전원공급장치", 65000, 2.0, 10, 0.00),
    ProductSpec("P-009", "공압 실린더", 78000, 1.5, 8, -0.15),
    ProductSpec("P-010", "베어링 6204", 6500, 4.5, 80, 0.00),
    ProductSpec("P-011", "산업용 릴레이", 12000, 3.0, 50, 0.05),
    ProductSpec("P-012", "방열 팬 24V", 9500, 2.0, 30, 0.25),
]

COMPANY_NAMES = [
    "한빛정밀", "대성기계", "미래오토메이션", "새봄전자", "누리금속",
    "해든로보틱스", "우리엔지니어링", "가온반도체", "푸른산업", "동서기계",
    "다온테크", "온누리전기", "청솔설비", "은하시스템", "라온메카닉스",
]

BASE_ORDERS_PER_DAY = 5.0
WEEKDAY_FACTOR = [1.2, 1.1, 1.0, 1.0, 0.9, 0.15, 0.05]  # 주말 거의 없음
BULK_ORDER_PROB = 0.02  # 프로젝트성 대량 주문 확률
BULK_ORDER_MULT = 4     # 대량 주문 시 주문 배수
AVG_EXTRA_ITEMS = 1.2  # 주문당 추가 상품 수의 평균

def make_customer(rng: np.random.Generator) -> pd.DataFrame:
    """COMPANY_NAMES 기반으로 거래처 생성"""
    used = set()
    rows = []
    for name in COMPANY_NAMES:
        while True:
            bn = f'{rng.integers(101, 999)}-{rng.integers(10,99)}-{rng.integers(10000, 99999)}'
            if bn not in used:
                used.add(bn)
                break

        # 거래처 규모: 큰 거래처는 자주, 많이 주문
        weight = float(rng.lognormal(mean=0.0, sigma=0.6))
        rows.append({'company_name':name, 'business_number':bn, 'weight':weight})

    df = pd.DataFrame(rows)
    df['p'] = df['weight'] / df['weight'].sum()     # 발생 확률
    df['size_mult'] = df['weight'] / df['weight'].mean()    # 평균 대비 거래처 규모 배수

    return df

def make_surges(rng: np.random.Generator, days: int) -> dict[str, tuple[int, int]]:
    """
    무작위 상품 3개에 약 3주짜리 프로젝트성 수요 급증 구간을 설정
    평소 상태 확인을 위해 급증 구간이 데이터 맨 앞이나 맨 뒤에 붙지 않게 한다.

    days : 더미데이터 전체 기간의 일수
    """
    surges = {}
    chosen = rng.choice(len(PRODUCTS), size=3, replace=False)
    for i in chosen:
        start = int(rng.integers(20, max(21, days - 30)))   # 급증 시작일
        surges[PRODUCTS[i].sku] = (start, start + 21)   # 급증 구간

    return surges

def product_weight(spec: ProductSpec, t: int, days: int, day: datetime, surges) -> float:
    """
    특정 시점(t일차)에 해당 상품이 주문에 뽑힐 상대적 가중치(점수)를 계산

    = 기본 인기도(popularity) * 시간에 따른 증감률(trend) * 단기 수요 급증(surge)
    """
    trend = 1 + spec.trend * (t / days)

    surge = 1.0
    if spec.sku in surges and surges[spec.sku][0] <= t <= surges[spec.sku][1]:
        surge = 1.8

    return spec.popularity * trend * surge

def generate(days: int, seed: int) -> pd.DataFrame:
    """하루씩 돌면서 그날 들어올 주문을 만들어내는 함수"""
    rng = np.random.default_rng(seed)
    customers = make_customer(rng)
    surges = make_surges(rng, days)

    now = datetime.now().replace(second=0, microsecond=0)
    start = (now - timedelta(days=days)).replace(hour=0, minute=0)  # 시작 날짜

    rows = []
    order_no = 1000
    for t in range(days + 1):
        day = start + timedelta(days=t)
        expected = BASE_ORDERS_PER_DAY * WEEKDAY_FACTOR[day.weekday()]  # 예상 주문 건수
        if day.day <= 7:    # 월초는 정기 발주 시기라 1.25배
            expected *= 1.25

        scores = np.array([product_weight(p, t, days, day, surges) for p in PRODUCTS])
        probs = scores / scores.sum()   # 해당 상품이 주문에 뽑힐 확률

        for _ in range(rng.poisson(expected)):
            ts = day + timedelta(hours=int(rng.integers(9, 18)), minutes=int(rng.integers(0, 60)))  # 주문 시각(9~17시)
            if ts > now:
                continue

            c = customers.iloc[int(rng.choice(len(customers), p=customers['p'].values))]
            n_items = min(1 + int(rng.poisson(AVG_EXTRA_ITEMS)), len(PRODUCTS))     # 주문할 상품 종류 수
            picked = rng.choice(len(PRODUCTS), size=n_items, replace=False, p=probs)    # 주문할 상품
            bulk = BULK_ORDER_MULT if rng.random() < BULK_ORDER_PROB else 1     # 대량 주문 배수

            order_no += 1
            for i in picked:
                spec = PRODUCTS[int(i)]
                qty = max(1, int(rng.poisson(spec.typical_qty * c['size_mult'] * bulk)))
                rows.append({
                    'order_id':order_no,
                    'ordered_at':ts.strftime('%Y-%m-%d %H:%M:%S'),
                    'business_number':c['business_number'],
                    'company_name':c['company_name'],
                    'sku':spec.sku,
                    'product_name':spec.name,
                    'quantity':qty,
                    'unit_price':spec.price,
                })

    return pd.DataFrame(rows)

def main():
    parser = argparse.ArgumentParser(description='더미 주문 CSV 생성')
    parser.add_argument('--days', type=int, default=365, help='오늘로부터 과거 며칠치 (기본 365)')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--out', type=str, default='data/dummy_orders.csv')
    args = parser.parse_args()

    df = generate(args.days, args.seed)

    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)

    df.to_csv(out, index=False, encoding='utf-8-sig')

    print(f'저장 완료: {out}')
    print(f'  행 수: {len(df):,} / 주문 수: {df["order_id"].nunique():,}')
    print(f'  기간: {df["ordered_at"].min()} ~ {df["ordered_at"].max()}')

if __name__ == '__main__':
    main()