from sqlalchemy import text
from database import engine

def verify():
    with engine.connect() as conn:
        total = conn.execute(text("SELECT COUNT(*) FROM apt_deal")).scalar()

        null_check = conn.execute(text("""
            SELECT
                COUNT(*) FILTER (WHERE 단지명 IS NULL) AS null_apt_name,
                COUNT(*) FILTER (WHERE 법정동 IS NULL) AS null_dong,
                COUNT(*) FILTER (WHERE 계약날짜 IS NULL) AS null_deal_date,
                COUNT(*) FILTER (WHERE 거래금액 IS NULL) AS null_deal_amount,
                COUNT(*) FILTER (WHERE 전용면적 IS NULL) AS null_area,
                COUNT(*) FILTER (WHERE 건축년도 IS NULL) AS null_build_year
            FROM apt_deal
        """)).fetchone()

        out_of_range = conn.execute(text("""
            SELECT COUNT(*) FROM apt_deal
            WHERE 거래금액 <= 0
                OR 전용면적 <= 0
                OR 층 > 100
        """)).scalar()

        invalid_date = conn.execute(text("""
            SELECT COUNT(*) FROM apt_deal
            WHERE 계약날짜 > CURRENT_DATE
        """)).scalar()

        negative_age = conn.execute(text("""
            SELECT COUNT(*) FROM apt_deal
            WHERE 건물연령 < 0
        """)).scalar()

        print('==== 검증 결과 ====')
        print(f'전체 건수 : {total}')
        print(f'단지명 NULL 건수 : {null_check[0]}')
        print(f'법정동 NULL 건수 : {null_check[1]}')
        print(f'계약날짜 NULL 건수 : {null_check[2]}')
        print(f'거래금액 NULL 건수 : {null_check[3]}')
        print(f'전용면적 NULL 건수 : {null_check[4]}')
        print(f'건축년도 NULL 건수 : {null_check[5]}')
        print(f'거래금액, 전용면적, 층 범위 이탈 건수 : {out_of_range}')
        print(f'계약날짜 이상치 건수 : {invalid_date}')
        print(f'건물연령 음수 건수 : {negative_age}')

        ok = (
            total > 0
            and all(value == 0 for value in null_check)
            and out_of_range == 0
            and invalid_date == 0
            and negative_age == 0
        )
        print(f'결과 : {"PASS" if ok else "FAIL"}')
        return ok
    
if __name__ == '__main__':
    verify()