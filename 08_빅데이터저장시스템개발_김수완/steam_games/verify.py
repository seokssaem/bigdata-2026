# ==================================================================
# steam_games/verify.py
#
#   Steam 게임 데이터 적재 검증
#       - 원본 대비 완전성 (원본 유효건수 = DB 건수)
#       - games 필수 컬럼 NULL 여부
#       - 이상치 (가격/리뷰수 음수, 할인율·메타크리틱 범위 이탈,
#                 owners_min > owners_max)
#       - 자식 테이블 업무 키(app_id + 이름) 중복 여부
#       - 자식 테이블 -> games 참조 무결성(고아 레코드) 여부
# ==================================================================

import os
import pandas as pd
from sqlalchemy import text
from database import engine

BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'games.csv')

CHILD_TABLES = [
    ('game_genres', 'genre_name'),
    ('game_categories', 'category_name'),
    ('game_tags', 'tag_name'),
    ('game_developers', 'developer_name'),
    ('game_publishers', 'publisher_name'),
]


def _raw_valid_count() -> int:
    """
    원본 CSV의 '유효' 건수(비교 기준선) 계산
    - 원본은 헤더 39개/데이터 40필드로 밀려있으므로 usecols 없이 AppID, Name만 최소로 읽어서 확인
    - loader.py가 Name이 없는 행은 적재 대상에서 제외하므로, 여기서도 동일 기준으로 카운트
    """
    df = pd.read_csv(
        INPUT_PATH, header=None, skiprows=1,
        usecols=[0, 1], names=['AppID', 'Name'], encoding='utf-8-sig',
    )
    valid = df.dropna(subset=['AppID', 'Name'])
    return len(df), len(valid)


def verify():
    raw_total, raw_valid = _raw_valid_count()

    with engine.connect() as conn:
        # --- 1. 전체 적재 건수 ---
        db_total = conn.execute(text('SELECT COUNT(*) FROM games')).scalar()

        # --- 2. games 필수 컬럼 NULL 개수 ---
        null_check = conn.execute(text('''
            SELECT
                COUNT(*) FILTER (WHERE name IS NULL) AS null_name,
                COUNT(*) FILTER (WHERE price IS NULL) AS null_price,
                COUNT(*) FILTER (WHERE discount IS NULL) AS null_discount,
                COUNT(*) FILTER (WHERE owners_min IS NULL) AS null_owners_min,
                COUNT(*) FILTER (WHERE owners_max IS NULL) AS null_owners_max,
                COUNT(*) FILTER (WHERE peak_ccu IS NULL) AS null_peak_ccu,
                COUNT(*) FILTER (WHERE required_age IS NULL) AS null_required_age,
                COUNT(*) FILTER (WHERE metacritic_score IS NULL) AS null_metacritic,
                COUNT(*) FILTER (WHERE positive IS NULL) AS null_positive,
                COUNT(*) FILTER (WHERE negative IS NULL) AS null_negative
            FROM games
        ''')).fetchone()

        # --- 3. 이상치 확인 ---
        negative_price = conn.execute(text('SELECT COUNT(*) FROM games WHERE price < 0')).scalar()
        negative_review = conn.execute(text(
            'SELECT COUNT(*) FROM games WHERE positive < 0 OR negative < 0'
        )).scalar()
        invalid_discount = conn.execute(text(
            'SELECT COUNT(*) FROM games WHERE discount NOT BETWEEN 0 AND 100'
        )).scalar()
        invalid_metacritic = conn.execute(text(
            'SELECT COUNT(*) FROM games WHERE metacritic_score NOT BETWEEN 0 AND 100'
        )).scalar()
        invalid_owners_range = conn.execute(text(
            'SELECT COUNT(*) FROM games WHERE owners_min > owners_max'
        )).scalar()

        # --- 4. 자식 테이블: 업무 키 중복 + 참조 무결성 ---
        child_results = {}
        for table, name_col in CHILD_TABLES:
            dup = conn.execute(text(f'''
                SELECT COUNT(*) FROM (
                    SELECT app_id, {name_col}, COUNT(*) AS cnt
                    FROM {table}
                    GROUP BY app_id, {name_col}
                    HAVING COUNT(*) > 1
                ) t
            ''')).scalar()
            orphan = conn.execute(text(f'''
                SELECT COUNT(*) FROM {table} c
                LEFT JOIN games g ON c.app_id = g.app_id
                WHERE g.app_id IS NULL
            ''')).scalar()
            row_count = conn.execute(text(f'SELECT COUNT(*) FROM {table}')).scalar()
            child_results[table] = (row_count, dup, orphan)

    # --- 5. 결과 출력 ---
    print('==== Steam 게임 적재 검증 결과 ====')
    print(f'원본 CSV 전체 행수 : {raw_total:,}')
    print(f'원본 CSV 유효 행수(Name 결측 제외) : {raw_valid:,}')
    print(f'DB games 적재 건수 : {db_total:,}')
    print(f'games 필수 컬럼 NULL : {dict(null_check._mapping)}')
    print(f'가격 음수 : {negative_price}')
    print(f'리뷰수 음수 : {negative_review}')
    print(f'할인율 범위(0~100) 이탈 : {invalid_discount}')
    print(f'메타크리틱 점수(0~100) 범위 이탈 : {invalid_metacritic}')
    print(f'owners_min > owners_max 이상치 : {invalid_owners_range}')
    print()
    for table, (row_count, dup, orphan) in child_results.items():
        print(f'{table} : {row_count:,}건 / 중복키 {dup}건 / (games 미참조) {orphan}건')

    # --- 6. 최종 PASS/FAIL 판정 ---
    ok = (
        db_total == raw_valid
        and all(v == 0 for v in null_check)
        and negative_price == 0
        and negative_review == 0
        and invalid_discount == 0
        and invalid_metacritic == 0
        and invalid_owners_range == 0
        and all(dup == 0 and orphan == 0 for _, dup, orphan in child_results.values())
    )
    print()
    print(f'검증 결과 : {"PASS" if ok else "FAIL"}')
    return ok


if __name__ == '__main__':
    verify()
