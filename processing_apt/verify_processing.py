from sqlalchemy import text
from database import apt_engine, table_count

CHECKS = [
    (apt_engine, 'apt_dong_summary'),
    (apt_engine, 'apt_price_event_alerts')
]

def verify() -> bool:
    """각 테이블의 행 개수 반환하며 검증"""
    ok = True

    for engine, table_name in CHECKS:
        try:
            count = table_count(engine, table_name)
            print(f'{table_name}: {count}건')
        except Exception as exc:
            ok = False
            print(f'{table_name}: 확인 실패 - {exc}')
    
    print(f'[verify] 검증 결과: {"PASS" if ok else "FAIL"}')

    return ok