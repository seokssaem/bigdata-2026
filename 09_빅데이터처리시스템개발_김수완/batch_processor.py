# ================================================================================
# steam_games/batch_processor.py
#   - "배치 처리(Batch Processing)" 단계
#   - 저장시스템에 이미 적재되어 있는 원본 테이블(games, game_genres) 전체를
#          한 번에 읽어서, 집계 결과 테이블을 새로 만든다.
#
#   --> 배치 처리의 특징 : "전체 데이터를 대상으로, 정해진 시점에 한 번에" 처리
#       Python 코드가 데이터를 직접 계산하지 않고, PostgreSQL에게 SQL을 실행시켜
#       DB 엔진이 집계하도록 위임한다.
# ================================================================================
from database import engine, check_required_tables, execute_sql


def create_batch_genre_summary() -> None:
    """
    games 원본 데이터를 game_genres와 "app_id" 기준으로 조인한 뒤,
    "genre_name"(장르, 범주형 컬럼) 기준으로 그룹핑하여
    장르별 게임 수 / 평균 가격 / 평균 메타크리틱 점수 / 평균 긍정·부정 리뷰 수를 집계한다.

    ROUND(AVG(...)::numeric, 2)
        --> AVG 결과값을 numeric 타입으로 변환해라.
            PostgreSQL 문법 (::numeric)
            CAST(AVG(...) AS numeric)이 표준 SQL 문법
    """
    execute_sql(
        engine,
        '''
        DROP TABLE IF EXISTS batch_genre_summary;

        CREATE TABLE batch_genre_summary AS
        SELECT
            gg.genre_name,
            COUNT(*) AS game_count,
            ROUND(AVG(g.price)::numeric, 2) AS avg_price,
            ROUND(AVG(g.metacritic_score)::numeric, 2) AS avg_metacritic_score,
            ROUND(AVG(g.positive)::numeric, 2) AS avg_positive,
            ROUND(AVG(g.negative)::numeric, 2) AS avg_negative
        FROM games g
        JOIN game_genres gg ON g.app_id = gg.app_id
        GROUP BY gg.genre_name;

        CREATE INDEX idx_batch_genre_summary_count
        ON batch_genre_summary(game_count DESC);
        '''
    )
    print('[batch] 장르별 집계 완료: batch_genre_summary')


def run_batch_processing() -> None:
    """
    배치 처리 전체 흐름을 순서대로 실행하는 엔트리포인트(프로그램이 실행을 시작하는 지점) 함수

    실행 순서:
        1) check_required_tables() : 원본 테이블이 준비되었는지 확인
        2) create_batch_genre_summary() : 장르별 집계 테이블 생성

    작은 단위로 쪼개고, 함수가 순서대로 호출하는 구조는 pipeline.py에서
    batch / event 단계를 조립할 때 재사용하기 쉽다.
    """
    print('[batch] 필수 입력 테이블 확인')
    check_required_tables()
    create_batch_genre_summary()
    print('[batch] 배치 처리 완료')


# 이 파일을 python batch_processor.py 처럼 직접 실행했을 때만 아래 코드가 동작한다.
# (다른 파일에서 import batch_processor 로 불러올 때는 실행되지 않는다.
#   모듈 재사용을 위한 관용구)
if __name__ == '__main__':
    run_batch_processing()  # 엔트리포인트 함수 호출
