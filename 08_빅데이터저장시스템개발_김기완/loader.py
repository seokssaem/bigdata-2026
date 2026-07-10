import os
import pandas as pd
from database import get_session
from models import AirportCongestion

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'airport_congestion.csv')

def load_from_csv(path: str=INPUT_PATH) -> dict:
    df = pd.read_csv(path, encoding='utf-8-sig')
    df['수집일시'] = pd.to_datetime(df['수집일시'], errors='coerce').dt.date

    db = get_session()
    success = 0
    failed = 0

    print(f'[loader] 총 {len(df):,}건 데이터 적재 시작...')

    for _, row in df.iterrows():
        try:
            congestion = AirportCongestion(
                공항코드 = str(row['공항코드']),
                수집시간 = str(row['수집시간']),
                수집일시 = row['수집일시'],
                A구역_혼잡도 = float(row['A구역_혼잡도']) if pd.notna(row['A구역_혼잡도']) else None,
                B구역_혼잡도 = float(row['B구역_혼잡도']) if pd.notna(row['B구역_혼잡도']) else None,
                C구역_혼잡도 = float(row['C구역_혼잡도']) if pd.notna(row['C구역_혼잡도']) else None,
                전체_혼잡도 = float(row['전체_혼잡도']) if pd.notna(row['전체_혼잡도']) else None,
                혼잡여부 = str(row['혼잡여부']) if pd.notna(row['혼잡여부']) else None,
            )
            db.merge(congestion)
            success += 1
            
            if success % 1000 == 0:
                db.commit()
        except Exception as e:
            db.rollback()
            failed += 1
            print(f'적재 실패 - {row.get("공항코드")} / {e}')

    db.commit()
    db.close()

    print(f'[loader] 적재 완료 - 성공: {success:,}건 / 실패: {failed:,}건')
    return {'success': success, 'failed': failed}

if __name__ == '__main__':
    load_from_csv()