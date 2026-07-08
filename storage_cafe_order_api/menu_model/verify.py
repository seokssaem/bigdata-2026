from sqlalchemy import text  
from database import engine

def verify():
   
    with engine.connect() as conn:

        # --- 1. 전체 건수 확인 ---
        total = conn.execute(text("SELECT COUNT(*) FROM menu")).scalar()
        

        # --- 2. 필수 컬럼별 NULL 갯수 확인 ---
        null_check = conn.execute(text("""
            SELECT  COUNT(*) FILTER (WHERE 메뉴코드 IS NULL) AS null_station_code,
                    COUNT(*) FILTER (WHERE 메뉴명 IS NULL) AS null_station_name,
                    COUNT(*) FILTER (WHERE 가격 IS NULL) AS null_station_price
                   
            FROM menu """)).fetchone() 
        
        # --- 3. 가격의 음수 여부 확인 ---
        negative_count = conn.execute(text("""
            SELECT  COUNT(*) FROM menu
            WHERE 가격 < 0  """)).scalar()
        
               
    # --- 4. 검증 결과 출력---
    print('=== 커페 메뉴 적재 검증 결과 ===')
    print(f'전체 건수 : {total:,}')
    print(f'메뉴코드 NULL 건수 : {null_check[0]}')
    print(f'역명 NULL 건수 : {null_check[1]}')
    print(f'메뉴명 NULL 건수 : {null_check[2]}')
    print(f'가격 : {negative_count}')

    # --- 8. 최종 PASS/FAIL 판정 ---
    ok = (

        total > 0 
        and all(value == 0 for value in null_check)  # 모든 컬럼이 0이여야 통과
        and negative_count == 0
    )
    print(f'검증 결과 :  {"PASS" if ok else "FAIL"}')
    return ok

if __name__ == "__main__": 
    verify()