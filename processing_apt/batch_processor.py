from database import apt_engine, check_required_table, execute_sql

def create_apt_dong_summary() -> None:
    """법정동별 집계"""
    execute_sql(
        apt_engine,
        '''
        DROP TABLE IF EXISTS apt_dong_summary;

        CREATE TABLE apt_dong_summary AS
        SELECT
            "법정동" AS law_dong,
            COUNT(*) AS row_count,
            ROUND(AVG("평당가격")::numeric, 2) AS avg_price_per_area,
            ROUND(AVG("거래금액")::numeric, 2) AS avg_deal_amount
        FROM apt_deal
        GROUP BY "법정동";

        CREATE INDEX idx_apt_dong_summary_average
        ON apt_dong_summary(avg_price_per_area DESC);
        '''
    )
    print('[batch] 법정동별 집계 완료 : apt_dong_summary')

def run_batch_processing() -> None:
    """배치 처리 실행"""
    print('[batch] 필수 테이블 확인')
    check_required_table()
    create_apt_dong_summary()
    print('[batch] 배치 처리 완료')