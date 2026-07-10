# ===========================================================
# TEST/08_빅데이터저장시스템개발_김동욱/verify.py
#
#   수질검사/행정구역 적재 검증
#       - 필수 컬럼 NULL 여부
#       - 식수 적합 여부 (먹는 물 수질 기준)
#       - 원본 대비 완전성 (원본 건수 = DB 건수)
# ===========================================================
import os
import pandas as pd
from sqlalchemy import text
from database import engine

BASE_DIR = os.getcwd()
INPUT_PATH1 = os.path.join(BASE_DIR, "input", "water.csv")
INPUT_PATH2 = os.path.join(BASE_DIR, "input", "area.csv")

def verify():
    with engine.connect() as conn:
        # ---------- 완전성 검증 (원본 CSV 건수 = DB 건수) ----------
        df_water = pd.read_csv(INPUT_PATH1, encoding="utf-8-sig")
        df_area = pd.read_csv(INPUT_PATH2, encoding="utf-8-sig")
        csv_water_count = len(df_water)
        csv_area_count = len(df_area)

        db_water_count = conn.execute(text("SELECT COUNT(*) FROM water")).scalar()
        db_area_count = conn.execute(text("SELECT COUNT(*) FROM area")).scalar()

        # ---------- NULL 검증 (필수 컬럼 전체를 한 번의 쿼리로 집계) ----------
        null_water = conn.execute(text(
            """
            SELECT COUNT(*) FILTER (WHERE 정수장 IS NULL) AS null_plant,
                   COUNT(*) FILTER (WHERE 구분 IS NULL) AS null_type,
                   COUNT(*) FILTER (WHERE ph IS NULL) AS null_ph,
                   COUNT(*) FILTER (WHERE 탁도 IS NULL) AS null_turbidity,
                   COUNT(*) FILTER (WHERE 잔류염소 IS NULL) AS null_chlorine,
                   COUNT(*) FILTER (WHERE 검사시기 IS NULL) AS null_date
            FROM water
            """
        )).fetchone()

        null_area = conn.execute(text(
            """
            SELECT COUNT(*) FILTER (WHERE 정수장 IS NULL) AS null_plant,
                   COUNT(*) FILTER (WHERE 구군 IS NULL) AS null_gugun,
                   COUNT(*) FILTER (WHERE 행정구역 IS NULL) AS null_dong,
                   COUNT(*) FILTER (WHERE 급수분류 IS NULL) AS null_type
            FROM area
            """
        )).fetchone()

        water_null_total = sum(null_water)
        area_null_total = sum(null_area)

        # ---------- 이상치 검증 (먹는 물 수질 기준) ----------
        # pH 농도 : 5.8 ~ 8.5
        # 탁도 : 0.5 NTU 이하
        # 잔류염소 : 0.1 ~ 4.0 mg/L

        abnormal_ph = conn.execute(text(
            """
            SELECT 정수장, 구분, 검사시기, ph FROM water
            WHERE ph < 5.8 OR ph > 8.5
            """
        )).fetchall()

        abnormal_turbidity = conn.execute(text(
            """
            SELECT 정수장, 구분, 검사시기, 탁도 FROM water
            WHERE 탁도 > 0.5
            """
        )).fetchall()

        abnormal_chlorine = conn.execute(text(
            """
            SELECT 정수장, 구분, 검사시기, 잔류염소 FROM water
            WHERE 잔류염소 < 0.1 OR 잔류염소 > 4.0
            """
        )).fetchall()

    print(f"1. 완전성 검증")
    print(f"water - 원본 CSV: {csv_water_count}건 / DB: {db_water_count}건 ")
    print(f"area  - 원본 CSV: {csv_area_count}건 / DB: {db_area_count}건 ")

    print(f"\n2. NULL 검증")
    print(f"water 필수 컬럼 NULL 합계: {water_null_total}건")
    print(f"area 필수 컬럼 NULL 합계: {area_null_total}건")

    print(f"\n3. 이상치 검증 (먹는 물 수질 기준)")
    print(f"ph 농도 기준 부적합 : {len(abnormal_ph)}건")
    for row in abnormal_ph:
        print(f"- {row[0]} {row[1]} {row[2]} ph={row[3]}")

    print(f"탁도 기준 부적합 : {len(abnormal_turbidity)}건")
    for row in abnormal_turbidity:
        print(f"- {row[0]} {row[1]} {row[2]} 탁도={row[3]}")

    print(f"잔류염소 기준 부적합 : {len(abnormal_chlorine)}건")
    for row in abnormal_chlorine:
        print(f"- {row[0]} {row[1]} {row[2]} 잔류염소={row[3]}")

    ok = (
        csv_water_count == db_water_count
        and csv_area_count == db_area_count
        and water_null_total == 0
        and area_null_total == 0
        and len(abnormal_ph) == 0
        and len(abnormal_turbidity) == 0
        and len(abnormal_chlorine) == 0
    )
    print(f"\n검증 결과 : {ok}")
    return ok


if __name__ == "__main__":
    verify()