import os
import pandas as pd
from database import engine, get_session
from models import AptDeal

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'apt_deal.csv')

def load_from_csv(path :str=INPUT_PATH) -> dict:
    df = pd.read_csv(path, encoding='utf-8-sig')

    db = get_session()
    success = 0
    failed = 0
    
    for _, row in df.iterrows():
        try:
            deal = AptDeal(
                단지명=str(row['단지명']),
                법정동=str(row['법정동']),
                계약날짜=row['계약날짜'],
                거래금액=int(row['거래금액']),
                평당가격=float(row['평당가격']) if pd.notna(row['평당가격']) else None,
                전용면적=float(row['전용면적']),
                층=int(row['층']) if pd.notna(row['층']) else None,
                층구간=str(row['층구간']) if pd.notna(row['층구간']) else None,
                건축년도=int(row['건축년도']),
                건물연령=int(row['건물연령']) if pd.notna(row['건물연령']) else None
            )
            db.add(deal)
            db.commit()
            success += 1

        except Exception as e:
            db.rollback()
            failed += 1
            print(f'[loader] 적재실패 - {e}')
        
    db.close()
    print(f'[loader] 적재완료 - 성공 {success}건 / 실패 {failed}건')

    return {'success':success, 'failed':failed}