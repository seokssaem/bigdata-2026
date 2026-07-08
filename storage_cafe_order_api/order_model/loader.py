import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import Order

BASE_DIR = os.getcwd()  #현재 파이썬 프로그램이 실행되고 있는 작업 폴더의 경로를 문자열로 반환
ORDERS_PATH = os.path.join(BASE_DIR, 'input', 'orders.csv')

def load_orders(path: str = ORDERS_PATH) -> dict:
   
    df = pd.read_csv(path, encoding='utf-8-sig')
    df['주문일시'] = pd.to_datetime(df['주문일시'], errors='coerce') # 날짜로 변환할 수 없는 값은 오류를 발생시키는 대신 NaT(Not a Time)
    df = df.dropna(subset=['주문일시', '테이블번호', '메뉴코드', '수량']) # dropna()는 결측값(NaN, NaT 등)이 있는 행을 삭제

    records = df[['주문일시', '테이블번호', '메뉴코드', '수량']].to_dict(orient='records')


    # 저장할 데이터가 있는지 확인한 후, 데이터베이스에 데이터를 삽입하고, 중복된 데이터는 건너뛰는 과정
    if not records: # 저장할 데이터가 하나도 없으면 함수를 종료
        return {'success': 0, 'skipped_duplicate': 0, 'failed': 0}

    try:
        with engine.begin() as conn:
            stmt = pg_insert(Order).values(records)  # pg_insert는 PostgreSQL 전용 INSERT 문
            stmt = stmt.on_conflict_do_nothing(constraint='uq_orders_key') # 중복된 데이터가 있으면 오류를 내지 말고 그냥 건너뛰어라
            result = conn.execute(stmt)

        inserted = result.rowcount if result.rowcount is not None else 0  # 실제로 INSERT된 행의 개수
        skipped = len(records) - inserted

        print(f'[loader] orders 적재 완료 - 신규 {inserted}건 / 중복스킵 {skipped}건')
        return {'success': inserted, 'skipped_duplicate': skipped, 'failed': 0}

    except Exception as e:   # 오류가 발생하면 except에서 처리할 수 있도록 준비
        print(f'orders 적재 실패: {e}')
        return {'success': 0, 'skipped_duplicate': 0, 'failed': len(records)}


if __name__ == '__main__':
    load_orders()