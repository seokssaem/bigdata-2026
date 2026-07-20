from sqlalchemy import text
from database import lottery_engine, table_count

CHECKS = [
    (lottery_engine, 'address_lottery_event_alerts'),
    (lottery_engine, 'address_lottery_win_summary')
]

def verify() -> bool:
    print('==== 처리시스템 결과 검증 (배치 + 이벤트) ====')

    ok = True

    for engine, table_name in CHECKS:
        try:
            count = table_count(engine, table_name)
            print(f'{table_name}: {count:,}건')

        except Exception as exc:
            ok = False
            print(f'{table_name}: 확인 실패 - {exc}')
    
    print(f'검증 결과: {"PASS" if ok else "FAIL"}')

    return ok

if __name__ =='__main__':
    verify()