from database import execute_sql, subway_engine, table_count

def check_subway_table():
    """subway_raw 테이블 존재 여부, 데이터 건수 확인"""
    check = [(subway_engine, 'subway_raw', '지하철 저장시스템 실습 결과가 필요합니다.')]
    for engine, table_name, hint in check:
        try:
            count = table_count(engine, table_name)
            print(f'[batch] 입력 테이블 확인 완료: {table_name} {count:,}건')
        except Exception as exc:
            # 테이블 자체가 없거나 DB 접속이 안되는 경우 (원인 exc를 함께 보존)
            raise RuntimeError(f'{table_name} 테이블을 확인할 수 없습니다. {hint} 원인 : {exc}') from exc
        if count == 0:
            # 테이블은 있지만 적재된 행이 0건인 경우
            raise RuntimeError(f'{table_name} 테이블은 존재하지만 데이터가 없습니다. 저장시스템 적재를 먼저 확인하세요.')

def create_daily_summary() -> None:
    """날짜별 승차·하차 집계"""
    execute_sql(
        subway_engine,
        '''
        DROP TABLE IF EXISTS traffic_daily_summary;

        CREATE TABLE traffic_daily_summary AS
        SELECT
            "날짜" AS use_date,
            "승하차" AS ride_type,
            COUNT(*) AS row_count,
            SUM("인원수") AS total_passengers
        FROM subway_raw
        GROUP BY "날짜", "승하차"
        ORDER BY "날짜", "승하차";
        '''
    )
    print('[batch] 날짜별 승차·하차 집계 완료: traffic_daily_summary')

def run_batch_processing() -> None:
    """배치 처리 실행 함수"""
    print('[batch] 날짜별 배치 처리 시작')
    check_subway_table()
    create_daily_summary()
    print('[batch] 날짜별 배치 처리 완료')

if __name__ == '__main__':
    run_batch_processing()