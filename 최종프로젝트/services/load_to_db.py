"""
지금까지 만든 데이터(전처리, 카테고리, 등락률, 예측 결과)를 PostgreSQL에 적재하는 스크립트.

전제: services/preprocessing.py, categorize.py, analysis.py, predictor.py를
먼저 실행해서 data/ 폴더에 결과 파일들이 만들어져 있어야 한다.
"""
import pandas as pd
from sqlalchemy.orm import Session

from database import engine, SessionLocal, Base
import models
from services.aggregation import aggregate_prices


def _clean(value):
    """pandas의 NaN(값 없음)을 DB의 NULL(None)로 바꾼다. 아니면 일반 숫자로 변환."""
    return None if pd.isna(value) else float(value)


def load_products(db: Session, category_map: dict[str, str]) -> dict[str, int]:
    """상품명→category 매핑을 받아 products 테이블에 적재하고, 상품명→id 딕셔너리를 반환."""
    name_to_id = {}
    for name, category in category_map.items():
        product = db.query(models.Product).filter_by(product_name=name).first()
        if product is None:
            product = models.Product(product_name=name, category=category)
            db.add(product)
            db.flush()  # id를 바로 받아오기 위해
        elif product.category != category:
            product.category = category  # 정답표가 바뀌었으면 DB에도 반영
        name_to_id[name] = product.id
    db.commit()
    return name_to_id


def clear_derived_tables(db: Session):
    """
    가격이력/등락률/예측 테이블을 전부 비운다. (products는 유지)

    이 세 테이블은 CSV에서 계산해서 만드는 "파생 데이터"라서, 적재할 때마다
    통째로 새로 채우는 게 맞다. 예전처럼 "이미 있으면 건너뛰기"만 하면,
    집계 기준(표본 필터 등)을 바꾼 뒤 다시 적재해도 옛 행이 DB에 그대로 남는다.
    """
    db.query(models.Prediction).delete()
    db.query(models.PriceChange).delete()
    db.query(models.PriceHistory).delete()
    db.commit()


def load_price_history(db: Session, agg_df: pd.DataFrame, name_to_id: dict[str, int]):
    """상품×조사일 평균가격을 price_history 테이블에 적재."""
    for _, row in agg_df.iterrows():
        product_id = name_to_id.get(row["상품명"])
        if product_id is None:
            continue
        exists = db.query(models.PriceHistory).filter_by(
            product_id=product_id, survey_date=row["조사일"].date()
        ).first()
        if exists:
            continue
        db.add(models.PriceHistory(
            product_id=product_id,
            survey_date=row["조사일"].date(),
            avg_price=row["평균가격"],
        ))
    db.commit()
def load_price_changes(db: Session, analysis_df: pd.DataFrame, name_to_id: dict[str, int]):
    """등락률 계산 결과를 price_changes 테이블에 적재."""
    for _, row in analysis_df.iterrows():
        product_id = name_to_id.get(row["상품명"])
        if product_id is None:
            continue
        exists = db.query(models.PriceChange).filter_by(
            product_id=product_id, survey_date=row["조사일"].date()
        ).first()
        if exists:
            continue
        db.add(models.PriceChange(
            product_id=product_id,
            survey_date=row["조사일"].date(),
            avg_price=row["평균가격"],
            prev_price=_clean(row.get("이전가격")),
            price_diff=_clean(row.get("차액")),
            change_rate=_clean(row.get("등락률")),
            yoy_price=_clean(row.get("전년동기가격")),
            yoy_diff=_clean(row.get("전년동기차액")),
            yoy_change_rate=_clean(row.get("전년동기등락률")),
        ))
    db.commit()


def load_predictions(db: Session, pred_df: pd.DataFrame, name_to_id: dict[str, int]):
    """가격 예측 결과를 predictions 테이블에 적재 (상품당 최신 1건으로 갱신)."""
    for _, row in pred_df.iterrows():
        product_id = name_to_id.get(row["상품명"])
        if product_id is None:
            continue
        existing = db.query(models.Prediction).filter_by(product_id=product_id).first()
        if existing:
            existing.base_price = row["기준가격"]
            existing.predicted_price = row["예측가격"]
            existing.expected_change_rate = row["예상등락률"]
            existing.raw_expected_change_rate = row["원본예측등락률"]
        else:
            db.add(models.Prediction(
                product_id=product_id,
                base_price=row["기준가격"],
                predicted_price=row["예측가격"],
                expected_change_rate=row["예상등락률"],
                raw_expected_change_rate=row["원본예측등락률"],
            ))
    db.commit()


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        category_df = pd.read_csv("data/category_mapping.csv", encoding="utf-8-sig")
        category_map = dict(zip(category_df["상품명"], category_df["카테고리"]))
        name_to_id = load_products(db, category_map)
        print(f"products 적재 완료: {len(name_to_id)}개")

        clear_derived_tables(db)
        print("가격이력/등락률/예측 테이블 초기화 완료 (새로 적재)")

        raw = pd.read_pickle("data/prices_combined.pkl")
        agg = aggregate_prices(raw)
        load_price_history(db, agg, name_to_id)
        print(f"price_history 적재 완료: {db.query(models.PriceHistory).count()}행")

        analysis_df = pd.read_pickle("data/analysis_result.pkl")
        load_price_changes(db, analysis_df, name_to_id)
        print(f"price_changes 적재 완료: {db.query(models.PriceChange).count()}행")

        pred_df = pd.read_csv("data/price_predictions.csv", encoding="utf-8-sig")
        load_predictions(db, pred_df, name_to_id)
        print(f"predictions 적재 완료: {db.query(models.Prediction).count()}개")

    finally:
        db.close()


if __name__ == "__main__":
    run()
