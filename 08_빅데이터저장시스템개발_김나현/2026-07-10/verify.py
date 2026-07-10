# ===========================================================
# 기술은행 수요기술 조회 서비스/verify.py
# ===========================================================================

from sqlalchemy import text
from database import engine

def verify():
    # engine.connect()로 커넥션을 열고,  with 블록을 벗어나면 자동으로 연결 반환(close됨)
    with engine.connect() as conn:

        # --- 1. 전체 적재 건수 확인 ---
        # .scalar() --> 결과에서 첫번째 행의 첫번째 컬럼 값 하나만 뽑아온다.
        #               (값이 하나만 나오는 쿼리에 사용)
        total = conn.execute(text("SELECT COUNT(*) FROM tech")).scalar()

        # --- 2. 필수 컬럼별 NULL 개수 확인 ---
        # FILTER (WHERE 조건) --> 하나의 SELECT 안에서 조건별로 COUNT를 따로 집계하는
        #                           PostgreSQL의 문법
        null_check = conn.execute(text("""
            SELECT
                COUNT(*) FILTER (WHERE 수요기술번호 IS NULL) AS null_station_no,
                COUNT(*) FILTER (WHERE 수요기술명 IS NULL) AS null_station_name,
                COUNT(*) FILTER (WHERE 진행상태 IS NULL) AS null_date,
                COUNT(*) FILTER (WHERE 키워드 IS NULL) AS null_time_col,
                COUNT(*) FILTER (WHERE 기술도입지원기관 IS NULL) AS null_inout,
                COUNT(*) FILTER (WHERE 기술센터지역 IS NULL) AS null_count,
                COUNT(*) FILTER (WHERE 정보충실도 IS NULL) AS null_start_hour
            FROM tech
            """)).fetchone() # 결과가 7개의 컬럼으로 이루어진 한 행이므로, 튜플 형태의 행 하나를 가져온다
        
        # --- 3. 정보충실도 음수 여부 확인 ---
        negative_count = conn.execute(text("""
            SELECT COUNT(*) FROM tech 
            WHERE 정보충실도 < 0
        """)).scalar()

        # --- 4. 기술센터지역 값 유효성 확인 ---
        # 반드시 '대구', '충남', '충북', '광주', '울산', '전북', '경기', '부산', '경북', '경남', '포항', '서울', '전남', '대전', '인천', '강원', '경기대진', '제주' 
        # 중 하나의 문자열이어야 한다.
        invalid_inout = conn.execute(text("""
            SELECT COUNT(*) FROM tech
            WHERE 기술센터지역 NOT IN ('대구', '충남', '충북', '광주', '울산', '전북', '경기', '부산', '경북', '경남', '포항', '서울', '전남', '대전', '인천', '강원', '경기대진', '제주')
        """)).scalar()

        # --- 5. 업무 키(business key) 조합 중복 확인 ---
        # 업무 키 = 수요기술명, 진행상태, 기술도입지원기관 

        duplicate_count = conn.execute(text("""
            SELECT COUNT(*)
            FROM (
                SELECT 수요기술명, 진행상태, 기술도입지원기관, COUNT(*) AS cnt
                FROM tech
                GROUP BY 수요기술명, 진행상태, 기술도입지원기관
                HAVING COUNT(*) > 1
            ) t
        """)).scalar()

    # --- 7. 검증 결과 출력 ---
    print('==== 기술은행 수요기술 적재 검증 결과 ====')
    print(f'전체 건수 : {total:,}')
    print(f'수요기술번호 NULL 건수 : {null_check[0]}')
    print(f'수요기술명 NULL 건수 : {null_check[1]}')
    print(f'진행상태 NULL 건수 : {null_check[2]}')
    print(f'키워드 NULL 건수 : {null_check[3]}')
    print(f'기술도입지원기관 NULL 건수 : {null_check[4]}')
    print(f'기술센터지역 NULL 건수 : {null_check[5]}')
    print(f'정보충실도 NULL 건수 : {null_check[6]}')
    print(f'정보충실도 음수 건수 : {negative_count}')
    print(f'기술센터지역 이상값 건수 : {invalid_inout}')
    print(f'중복 키 건수 : {duplicate_count}')

    # --- 8. 최종 PASS/FAIL 판정 ---
    ok = (
        total > 0
        and all(value == 0 for value in null_check) # 모든 컬럼이 0이어야 통과
        and negative_count == 0
        and invalid_inout == 0
        and duplicate_count == 0
    )
    print(f'검증 결과 : {"PASS" if ok else "FAIL"}')
    return ok
    
if __name__ == '__main__':
    verify()