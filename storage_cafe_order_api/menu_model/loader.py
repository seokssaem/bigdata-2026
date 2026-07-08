import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import Menu

BASE_DIR = os.getcwd()
MENU_PATH = os.path.join(BASE_DIR, 'input', 'menu.csv')

def load_menu(path: str = MENU_PATH) -> dict:
    
    df = pd.read_csv(path, encoding='utf-8-sig')

    from database import get_session
    db = get_session()
    success, failed = 0, 0

    for _, row in df.iterrows():
        try:
            m = Menu(
                메뉴코드=str(row['메뉴코드']),
                메뉴명=str(row['메뉴명']),
                가격=int(row['가격']),
            )
            db.merge(m)
            db.commit()
            success += 1
        except Exception as e:
            db.rollback()
            failed += 1
            print(f'menu 적재 실패 - {row.get("메뉴코드")} / {e}')

    db.close()
    print(f'[loader] menu 적재 완료 - 성공 {success}건 / 실패 {failed}건')
    return {'success': success, 'failed': failed}


if __name__ == '__main__':
    load_menu()
