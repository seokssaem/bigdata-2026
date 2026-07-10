# ================================================
# steam_games/loader.py
#
# Kaggle Steam Games Dataset(games.csv)을
# games / game_genres / game_categories / game_tags /
# game_developers / game_publishers 테이블에 적재
#
# *** 원본 CSV 컬럼 밀림 현상 보정 ***
#   원본 헤더는 39개인데 실제 데이터는 행마다 40개 필드다.
#   (`DiscountDLC count`라는 헤더 하나가 원래 `Discount`와
#    `DLC count` 두 컬럼이 합쳐지며 헤더가 1개 부족해진 것으로 추정)
#   pandas 기본 read_csv로 읽으면 헤더 수(39) < 데이터 필드 수(40)라서
#   첫 번째 데이터 값을 인덱스로 취급하고, 나머지 모든 컬럼명이
#   한 칸씩 밀려서 매핑된다. (AppID 컬럼에 실제로는 게임 이름이 들어가는 등)
#   -> header=None, skiprows=1 + 올바른 컬럼명 40개를 직접 지정해서 해결
# ================================================

# 라이브러리 불러오기
import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import Game, GameGenre, GameCategory, GameTag, GameDeveloper, GamePublisher

# 경로 설정 및 기본값 설정
BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'input', 'games.csv')
CHUNK_SIZE = 5000

# ------------------------------------------------
# 원본 CSV의 "잘못된" 헤더 (파일에 실제로 적혀 있는 39개)
# ------------------------------------------------
_RAW_HEADER = [
    'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU', 'Required age', 'Price',
    'DiscountDLC count', 'About the game', 'Supported languages', 'Full audio languages', 'Reviews',
    'Header image', 'Website', 'Support url', 'Support email', 'Windows', 'Mac', 'Linux',
    'Metacritic score', 'Metacritic url', 'User score', 'Positive', 'Negative', 'Score rank',
    'Achievements', 'Recommendations', 'Notes', 'Average playtime forever', 'Average playtime two weeks',
    'Median playtime forever', 'Median playtime two weeks', 'Developers', 'Publishers', 'Categories',
    'Genres', 'Tags', 'Screenshots', 'Movies',
]

# 실제 데이터에 맞게 보정한 40개 컬럼명
# ('DiscountDLC count' 한 개를 'Discount' + 'DLC count' 두 개로 분리)
CORRECT_COLUMNS = ['AppID'] + _RAW_HEADER[1:7] + ['Discount', 'DLC count'] + _RAW_HEADER[8:]

# 적재에 실제로 사용할 컬럼만 골라서 읽기속도/메모리 절약
USECOLS = [
    'AppID', 'Name', 'Release date', 'Estimated owners', 'Peak CCU', 'Required age', 'Price',
    'Discount', 'Metacritic score', 'Positive', 'Negative',
    'Developers', 'Publishers', 'Categories', 'Genres', 'Tags',
]


def _split_owners(text):
    """'0 - 20000' 형태의 문자열을 (owners_min, owners_max) 정수 튜플로 변환"""
    try:
        lo, hi = str(text).split('-')
        return int(lo.strip()), int(hi.strip())
    except (ValueError, AttributeError):
        return 0, 0


def _prepare_games_chunk(chunk: pd.DataFrame) -> list[dict]:
    """
    pandas로 읽어온 CSV 한 덩어리(chunk)를,
    games 테이블에 바로 넣을 수 있는 딕셔너리 리스트로 가공
    """
    chunk = chunk.copy()

    # 이름이 없는 행은 NOT NULL 제약과 맞지 않으므로 제거
    chunk = chunk.dropna(subset=['AppID', 'Name'])

    # 출시일 : 파싱 실패시 NULL 허용(Date, nullable=True)
    chunk['Release date'] = pd.to_datetime(
        chunk['Release date'], errors='coerce', format='mixed'
    ).dt.date

    # 추정 소유자수 '0 - 20000' -> owners_min / owners_max
    owners = chunk['Estimated owners'].apply(_split_owners)
    chunk['owners_min'] = owners.apply(lambda t: t[0])
    chunk['owners_max'] = owners.apply(lambda t: t[1])

    # 결측치 있는 숫자 컬럼은 0으로 채우기 (NOT NULL 제약 대응)
    for col in ['Price', 'Discount', 'Peak CCU', 'Required age', 'Metacritic score', 'Positive', 'Negative']:
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce').fillna(0)

    chunk['AppID'] = chunk['AppID'].astype(int)
    chunk['Name'] = chunk['Name'].astype(str).str.slice(0, 500)

    # CSV 컬럼명(공백 포함) -> DB 컬럼명으로 매핑 후, 필요한 컬럼만 골라 딕셔너리 리스트로 변환
    chunk = chunk.rename(columns={
        'AppID': 'app_id',
        'Name': 'name',
        'Release date': 'release_date',
        'Price': 'price',
        'Discount': 'discount',
        'Peak CCU': 'peak_ccu',
        'Required age': 'required_age',
        'Metacritic score': 'metacritic_score',
        'Positive': 'positive',
        'Negative': 'negative',
    })

    columns = [
        'app_id', 'name', 'release_date', 'price', 'discount',
        'owners_min', 'owners_max', 'peak_ccu', 'required_age',
        'metacritic_score', 'positive', 'negative',
    ]
    return chunk[columns].to_dict(orient='records')



def _prepare_child_records(chunk: pd.DataFrame, csv_col: str, name_field: str) -> list[dict]:
    """
    콤마로 여러 값이 들어있는 컬럼(csv_col)을 낱개로 쪼개서
    자식 테이블에 넣을 딕셔너리 리스트로 변환
    (예: Genres='Action,Early Access' -> [{app_id, genre_name:'Action'}, {app_id, genre_name:'Early Access'}])
    """
    records = []
    sub = chunk.dropna(subset=['AppID', csv_col])
    for app_id, raw in zip(sub['AppID'], sub[csv_col]):
        values = {v.strip() for v in str(raw).split(',') if v.strip()}  # set으로 chunk 내 자체중복 제거
        for v in values:
            records.append({'app_id': int(app_id), name_field: v[:200]})
    return records


def _bulk_upsert_games(records: list[dict]) -> tuple[int, int]:
    """
    games 테이블 적재 (자연키 app_id 보유 -> merge/upsert 방식)
    이미 있는 app_id면 값 갱신(UPDATE), 없으면 새로 삽입(INSERT)
    """
    if not records:
        return 0, 0

    stmt = pg_insert(Game).values(records)
    update_cols = {c.name: getattr(stmt.excluded, c.name)
                   for c in Game.__table__.columns if c.name != 'app_id'}
    stmt = stmt.on_conflict_do_update(index_elements=['app_id'], set_=update_cols)

    with engine.begin() as conn:
        result = conn.execute(stmt)
    # PostgreSQL upsert는 삽입/갱신 모두 rowcount에 포함되므로 성공 건수로만 집계
    return (result.rowcount if result.rowcount is not None else 0), 0


def _bulk_insert_ignore(model, records: list[dict], constraint: str) -> int:
    """
    자연키가 없는 자식 테이블 적재 (UNIQUE 제약 + ON CONFLICT DO NOTHING)
    이미 같은 (app_id, 값) 조합이 있으면 조용히 건너뛴다.
    """
    if not records:
        return 0
    stmt = pg_insert(model).values(records)
    stmt = stmt.on_conflict_do_nothing(constraint=constraint)
    with engine.begin() as conn:
        result = conn.execute(stmt)
    return result.rowcount if result.rowcount is not None else 0


# csv 컬럼명 -> (모델, 필드명, UNIQUE 제약이름)
_CHILD_TABLE_SPEC = [
    ('Genres', GameGenre, 'genre_name', 'uq_game_genres_key'),
    ('Categories', GameCategory, 'category_name', 'uq_game_categories_key'),
    ('Tags', GameTag, 'tag_name', 'uq_game_tags_key'),
    ('Developers', GameDeveloper, 'developer_name', 'uq_game_developers_key'),
    ('Publishers', GamePublisher, 'publisher_name', 'uq_game_publishers_key'),
]


def load_from_csv(path: str = INPUT_PATH, chunksize: int = CHUNK_SIZE) -> dict:
    """
    CSV 파일을 배치 단위로 읽어 games 및 자식 테이블에 적재하는 메인 함수

    반환값(리턴값)
    dict : 테이블별 적재 결과 요약
    """
    totals = {'games': 0, 'genres': 0, 'categories': 0, 'tags': 0, 'developers': 0, 'publishers': 0}
    total_failed = 0

    reader = pd.read_csv(
        path,
        header=None,
        skiprows=1,               # 원본(잘못된) 헤더 줄 건너뛰기
        names=CORRECT_COLUMNS,    # 보정된 40개 컬럼명 적용
        usecols=USECOLS,
        chunksize=chunksize,
        encoding='utf-8-sig',
    )

    for i, chunk in enumerate(reader):
        try:
            # 1) games 테이블 적재 (upsert)
            game_records = _prepare_games_chunk(chunk)
            inserted, _ = _bulk_upsert_games(game_records)
            totals['games'] += inserted

            # 2) 자식 테이블들 적재 (insert or ignore)
            for csv_col, model, field, constraint in _CHILD_TABLE_SPEC:
                child_records = _prepare_child_records(chunk, csv_col, field)
                key = {
                    'Genres': 'genres', 'Categories': 'categories', 'Tags': 'tags',
                    'Developers': 'developers', 'Publishers': 'publishers',
                }[csv_col]
                totals[key] += _bulk_insert_ignore(model, child_records, constraint)

            print(f'{i + 1}번째 배치 처리 완료 (games 누적 {totals["games"]:,}건)')

        except Exception as e:
            total_failed += len(chunk)
            print(f'{i + 1}번째 배치 실패(이 배치만 건너뛰고 다음 배치 계속 진행): {e}')

    print(
        '[loader] 전체 적재 완료 - '
        f'games: {totals["games"]:,} / genres: {totals["genres"]:,} / '
        f'categories: {totals["categories"]:,} / tags: {totals["tags"]:,} / '
        f'developers: {totals["developers"]:,} / publishers: {totals["publishers"]:,} / '
        f'실패건수: {total_failed:,}'
    )
    totals['failed'] = total_failed
    return totals


if __name__ == '__main__':
    load_from_csv()
