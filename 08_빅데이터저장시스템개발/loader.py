import os
import pandas as pd
from database import get_session
from models import lottery

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'data', 'lottery_win.csv')
CHUNK_SIZE = 5000

def load_from_csv(path: str = INPUT_PATH) -> dict:
    df = pd.read_csv(path, encoding='cp949')
    df['순번'] = pd.to_numeric(df['순번'], errors='coerce')
    df['자동당첨건수'] = pd.to_numeric(df['자동당첨건수'], errors='coerce')

    db = get_session()
    success= 0
    failed = 0

    for _, row in df. iterrows():
        try:
            Win = lottery(
                순번 = int(row['순번']),
                상호 = str(row['상호']),
                지역 = str(row['지역']),
                자동당첨건수 = int(row['자동당첨건수']) if pd.notna(row['자동당첨건수']) else None,
            )
            db.merge(Win)
            db.commit()
            success += 1
            
        except Exception as e:
            db.rollback()
            failed += 1
            print(f'적재실패 - {row.get("상호")} / {e}')

    db.close()
    print(f'적재완료 - 성공: {success:,}건 / 실패: {failed:,}건')

    return {'success' : success, 'failed' : failed}