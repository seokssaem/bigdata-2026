import os
import pandas as pd
from sqlalchemy import text
from database import engine

STATUS_LIST = {'원활', '보통', '혼잡'}
BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'airport_congestion.csv')

def verify(source_path: str = INPUT_PATH):
    try:
        df = pd.read_csv(source_path, encoding='utf-8-sig')
        source_count = len(df)
    except Exception:
        source_count = 0

    with engine.connect() as conn:
        db_count = conn.execute(text("SELECT COUNT(*) FROM airport_congestion")).scalar()

        null_check = conn.execute(text("""
            SELECT COUNT(*) FILTER (WHERE 전체_혼잡도 IS NULL) AS null_cnt
            FROM airport_congestion
        """)).fetchone()

        status_values = conn.execute(text(
            "SELECT DISTINCT 혼잡여부 FROM airport_congestion"
        )).fetchall()
        invalid_status = []
        for s in status_values:
            if s[0] not in STATUS_LIST and s[0] is not None:
                invalid_status.append(s[0])

    print('==== 적재 검증 결과 ====')
    print(f'원본 데이터 건수 : {source_count:,} 건')
    print(f'DB 적재 데이터 건수 : {db_count:,} 건')
    print(f'전체_혼잡도 미입력(NULL) 건수 : {null_check[0]} 건')
    print(f'혼잡여부 이상값 : {invalid_status if invalid_status else "없음"}')

    is_complete = (source_count == db_count and source_count > 0)
    print(f'원본 대비 완전성 검증 결과 : {"통과" if is_complete else "실패"}')

if __name__ == '__main__':
    verify()