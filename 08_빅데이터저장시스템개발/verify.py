from sqlalchemy import text
from database import engine

def verify():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM lottery_win")).scalar()

        null_check = conn.execute(text("""
            SELECT  COUNT(*) FILTER (WHERE 상호 IS NULL) AS null_name,
                    COUNT(*) FILTER (WHERE 순번 IS NULL) AS null_seq,
                    COUNT(*) FILTER (WHERE 지역 IS NULL) AS null_region
                    FROM lottery_win"""
        )).fetchone()

        out_of_region = conn.execute(text(
            "SELECT COUNT(*) FROM lottery_win WHERE 지역 NOT LIKE '%서울%'"
        )).scalar()

    print('===적재 검증 결과 ===')
    print(f'전체 건수 : {total:,}')
    print(f'지역 범위 이탈 건수 : {out_of_region}')

    ok = (null_check[0] == 0 and null_check[1] == 0 and null_check[2] == 0 and out_of_region == 0)
    print(f'검증 결과 : PASS {ok}')

if __name__ == '__main':
    verify()