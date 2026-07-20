from database import airport_engine, table_count, execute_sql

def check_airport_input() -> int:
    try:
        count = table_count(airport_engine, "airport_congestion")
        print(f'[batch] 입력 테이블 확인 완료: airport_congestion {count:,}건')
        return count
    except Exception as exc:
        raise RuntimeError(f'airport_congestion 테이블을 확인할 수 없습니다. 원인: {exc}') from exc

def create_airport_batch_summary() -> None:
    execute_sql(
        airport_engine,
        '''
        DROP TABLE IF EXISTS traffic_airport_batch_summary;

        CREATE TABLE traffic_airport_batch_summary AS
        SELECT
            COALESCE("혼잡여부", '미분류') AS congestion_status,
            COUNT(*) AS row_count,
            ROUND(AVG("전체_혼잡도")::numeric, 2) AS avg_total_congestion
        FROM airport_congestion
        GROUP BY COALESCE("혼잡여부", '미분류');

        CREATE INDEX idx_traffic_airport_batch_status
        ON traffic_airport_batch_summary(congestion_status);
        '''
    )
    print('[batch] 범주형 기준 배치 집계 완료: traffic_airport_batch_summary')

def main() -> None:
    print('[batch] 배치 처리 시작')
    check_airport_input()
    create_airport_batch_summary()
    print('[batch] 배치 처리 완료')

if __name__ == '__main__':
    main()