# ================================================
# TEST/08_빅데이터저장시스템개발_김동욱/loader.py
#
# water.csv와 area.csv를 테이블에 적재
# ================================================
import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import Water, Area


BASE_DIR = os.getcwd()
INPUT_PATH1 = os.path.join(BASE_DIR, "input", "water.csv")
INPUT_PATH2 = os.path.join(BASE_DIR, "input", "area.csv")

def _prepare_water_df(df: pd.DataFrame) -> list[dict]:
    df = df.copy()    
    df["ph"] = pd.to_numeric(df["PH"], errors="coerce")
    df["탁도"] = pd.to_numeric(df["탁도"], errors="coerce")
    df["잔류염소"] = pd.to_numeric(df["잔류염소"], errors="coerce")
    df["검사시기"] = pd.to_datetime(df["검사시기"], format="%Y년 %m월", errors="coerce").dt.date

    df = df.dropna(subset=["정수장", "구분", "검사시기"])

    return df[["정수장", "구분", "ph", "탁도", "잔류염소", "검사시기"]].to_dict(orient="records")

def _prepare_area_df(df: pd.DataFrame) -> list[dict]:
    df = df.copy()
    df = df.dropna(subset=["정수장", "구군", "행정구역", "급수분류"])
    return df[["정수장", "구군", "행정구역", "급수분류"]].to_dict(orient="records")

def load_water_csv(path: str = INPUT_PATH1) -> dict:
    df = pd.read_csv(path, encoding="utf-8-sig")
    records = _prepare_water_df(df)

    if not records:
        print("[loader] water 적재할 데이터 없음")
        return {"success": 0, "skipped_duplicate": 0, "failed": 0}

    try:
        with engine.begin() as conn:
            stmt = pg_insert(Water).values(records)
            stmt = stmt.on_conflict_do_nothing(constraint="uq_water_key")
            result = conn.execute(stmt)

        inserted = result.rowcount if result.rowcount is not None else 0
        skipped = len(records) - inserted

        print(f"[loader] water 적재 완료 - 신규: {inserted:,}건 / 중복스킵: {skipped:,}건")
        return {"success": inserted, "skipped_duplicate": skipped, "failed": 0}

    except Exception as e:
        print(f"[loader] water 적재 실패 - {e}")
        return {"success": 0, "skipped_duplicate": 0, "failed": len(records)}

def load_area_csv(path: str = INPUT_PATH2) -> dict:
    df = pd.read_csv(path, encoding="utf-8-sig")
    records = _prepare_area_df(df)

    if not records:
        print("[loader] area 적재할 데이터 없음")
        return {"success": 0, "skipped_duplicate": 0, "failed": 0}

    try:
        with engine.begin() as conn:
            stmt = pg_insert(Area).values(records)
            stmt = stmt.on_conflict_do_nothing(constraint="uq_area_key")
            result = conn.execute(stmt)

        inserted = result.rowcount if result.rowcount is not None else 0
        skipped = len(records) - inserted

        print(f"[loader] area 적재 완료 - 신규: {inserted:,}건 / 중복스킵: {skipped:,}건")
        return {"success": inserted, "skipped_duplicate": skipped, "failed": 0}

    except Exception as e:
        print(f"[loader] area 적재 실패 - {e}")
        return {"success": 0, "skipped_duplicate": 0, "failed": len(records)}


if __name__ == "__main__":
    load_water_csv()
    load_area_csv()