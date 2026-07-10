# ================================================
# 기술은행 수요기술 조회 서비스/loader.py
#
# 수집한 결과로 나온 파일 NTB_db.csv을
# tech 테이블에 적재
# ================================================

# 라이브러리 불러오기
import os
import pandas as pd
from sqlalchemy.dialects.postgresql import insert as pg_insert
from database import engine
from models import Tech

# 경로 설정 및 기본값 설정
BASE_DIR = os.getcwd()
INPUT_PATH = os.path.join(BASE_DIR, 'data', 'NTB_db.csv')
CHUNK_SIZE = 5000

# CSV -> DB 배치 적재
def _prepare_chunk(chunk: pd.DataFrame) -> list[dict]:
    """
    pandas로 읽어온 CSV 한 덩어리(chunk)를, DB에 바로 넣을 수 있는
    딕셔너리 리스트 형태로 가공하는 함수
    """
    chunk = chunk.copy()  # 원본 chunk를 직접 건드리면 pandas에서 경고!

    chunk['수집일시'] = pd.to_datetime(chunk['수집일시'], errors='coerce').dt.date
    

    chunk = chunk.dropna(subset=['수요기술명', '진행상태', '기술도입지원기관'])

    return chunk[['희망구매유형',
                '수요기술명',
                '수요기술번호',
                '진행상태',
                '구매희망시기',
                '희망기술개요',
                '키워드',
                '기술도입지원기관',
                '기술지표상세',
                '기술구매조건',
                '기술이전계약설명',
                '기술이전계약유형',
                '정액기술료',
                '기타계약조건',
                '경상기술료',
                '기술센터지역',
                '수집일시',
                '정보충실도']].to_dict(orient='records') # 행단위로 하나씩 딕셔너리 만든다

# 함수 정의
def load_from_csv(path: str=INPUT_PATH, chunksize: int=CHUNK_SIZE) -> dict:
    """
    CSV 파일을 배치 단위로 읽어 tech 테이블에 적재하는 메인 함수

    매개변수(파라미터)
    path: str 
        --> 읽어들일 CSV 파일 경로
    chunksize: int
        --> 한 번에 읽어서 처리할 행의 개수(배치 크기)

    반환값(리턴값)
    dict
        {"success": 신규 적재 건수, "skipped_duplicate": 중복 스킵 건수, "failed": 실패 건수}
    
    """
    # 전체 적재 결과를 누적할 카운터들
    total_success = 0  # 새로 삽입된 건수
    total_skipped = 0  # UNIQUE 제약에 걸려 중복으로 스킵된 건수
    total_failed = 0  # 배치 자체가 에러로 실패한 건수

    for i, chunk in enumerate(pd.read_csv(INPUT_PATH, encoding='utf-8-sig', chunksize=CHUNK_SIZE)):
        # try:
        # 이번 배치(데이터를 한번에 처리하지 않고 일정한 묶음 단위로 처리)를 
        # DB 삽입용 딕셔너리 리스트로 가공
        records = _prepare_chunk(chunk)  # 함수 호출

        # 가공 후 남은 데이터가 없다면 (전부 결측 등으로 걸러졌다면) 이번 배치는 건너뛴다.
        if not records:
            continue

        with engine.begin() as conn:
            # PostgreSQL 전용 insert 구문 생성
            stmt = pg_insert(Tech).values(records)

            # UNIQUE 제약에 위반되는 행은 에러를 내지 않고 그냥 무시(skip) 하도록 설정
            stmt = stmt.on_conflict_do_nothing(constraint='uq_tech_key')

            # 실제 SQL 실행
            result = conn.execute(stmt)

        # rowcount : 실제로 삽입된 행의 개수 (충돌로 스킵된 행은 포함하지 않는다)
        # 일부 환경에서는 rowcount가 None일 수 있어 방어적으로 처리 (0표시)
        inserted = result.rowcount if result.rowcount is not None else 0

        # 중복이라 스킵된 건수 ==> 이번 배치에서 시도한 건수 - 실제 삽입된 건수
        skipped = len(records) - inserted

        total_success += inserted
        total_skipped += skipped

        print(f'{i+1}번째 배치 - 신규 {inserted}건 / 중복스킵 {skipped}건')

        # except Exception as e:
        #     # 예상치 못한 에러(예: 자료형 불일치)가 발생한 경우 이번 배치만 실패로 기록, 다음 넘어간다
        #     total_failed += len(chunk)
        #     print(f'{i+1}번째 배치 실패(이 배치만 롤백, 다음 배치 계속 진행): {e}')

    # 최종 결과를 딕셔너리로 정리 (다른 모듈에서 결과를 활용할 수 있도록 반환)
    summary = {
        "success": total_success,
        "skipped_duplicate": total_skipped,
        "failed": total_failed,
    }
    print(
        f'[loader] 전체 적재 완료 - 신규: {total_success:,}건 '
        f'/ 중복스킵: {total_skipped:,}건 '
        f'/ 실패 : {total_failed:,}건'
    )
    return summary


# 이 파일을 직접 실행했을 때만 (python loader.py) 아래 코드가 동작한다.
# 다른 모듈(파일)에서 import loader만 했을 때는 이 부분이 실행되지 않는다.
if __name__ == '__main__':
    load_from_csv() 