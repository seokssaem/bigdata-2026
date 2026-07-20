
from database import ntb_engine, check_required_tables, execute_sql

def create_tech_region_summary() -> None:
    """
    지역별 평균정보충실도 집계

    AVG("인원수")::numeric 
        --> AVG 결과값을 numeric타입으로 변환해라.
            PostgreSQL 문법
            CAST(AVG("인원수") AS numeric)이 표준 SQL문법    
    """
    execute_sql(
        ntb_engine,
        '''
        DROP TABLE IF EXISTS tech_region_summary;

        CREATE TABLE tech_region_summary AS
        SELECT
            "기술센터지역",
            COUNT(*) AS "기술수요건수",
            AVG("정보충실도") AS "평균정보충실도"
        FROM tech
        GROUP BY "기술센터지역";

        CREATE INDEX idx_tech_region_summary_total
        ON tech_region_summary("평균정보충실도" DESC);
        '''
    )
    print('[batch] 지역별 기술수요 및 평균 정보 충실도 집계: tech_region_summary')

def create_tech_status_summary() -> None:
    """
    진행상태별 집계
    """
    execute_sql(
        ntb_engine,
        '''
        DROP TABLE IF EXISTS tech_status_summary;

        CREATE TABLE tech_status_summary AS
        SELECT
            "진행상태",
            COUNT(*) AS "건수"
        FROM tech
        GROUP BY "진행상태";

        CREATE INDEX idx_tech_status_summary_count
        ON tech_status_summary("건수" DESC);
        ''',
    )
    print('[batch] 진행상태별 집계 : tech_status_summary')

def run_batch_processing() -> None:

    print('[batch] 필수 입력 테이블 확인')
    check_required_tables()
    create_tech_region_summary()
    create_tech_status_summary()
    print('[batch] 배치 처리 완료')

# 이 파일을 python batch_processor.py 처럼 직접 실행했을 때만 아래 코드가 작동한다.
# (다른 파일에서 import batch_processor로 불러오면 실행되지 않는다.)

if __name__ == '__main__':
    run_batch_processing()