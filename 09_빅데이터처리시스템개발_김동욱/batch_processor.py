# ===========================================================================
# 09_빅데이터처리시스템개발_김동욱/batch_processor.py
#     - 배치 처리 : 각 정수장 및 구분별 분기별 평균
# ===========================================================================
from database import water_engine, check_required_tables, execute_sql

def create_water_summary() -> None:
    """
    정수장 수질 검사 데이터(water)를 "정수장+구분+분기(검사시기에서 추출)" 기준으로
    그룹핑하여 정수장 및 구분별 분기별 수질검사 집계 테이블을 만든다.    
    """
    execute_sql(
        water_engine,
        """
        DROP TABLE IF EXISTS batch_water_summary;

        CREATE TABLE batch_water_summary AS
        SELECT
            정수장,
            구분,
            ROUND(AVG(ph)::numeric, 2) AS ph_평균,
            ROUND(AVG(탁도)::numeric, 2) AS 탁도_평균,
            ROUND(AVG(잔류염소)::numeric, 2) AS 잔류염소_평균,
            EXTRACT(QUARTER FROM 검사시기)::int AS 분기,
            COUNT(*) AS 표본개수
        FROM water
        GROUP BY 정수장, 구분, EXTRACT(QUARTER FROM 검사시기);
        """
    )
    print("[batch] 정수장별 분기별 수질검사 결과 집계 완료 : batch_water_summary")

def run_batch_processing() -> None:
    """
    배치 처리 전체 흐름을 순서대로 실행하는 엔트리포인트(프로그램이 실행을 시작하는 지점) 함수
    """
    print("[batch] 필수 입력 테이블 확인")
    check_required_tables()
    create_water_summary()
    print("[batch] 배치 처리 완료")

if __name__ == "__main__":
    run_batch_processing()