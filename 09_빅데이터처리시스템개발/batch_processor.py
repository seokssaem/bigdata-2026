from database import lottery_engine,check_required_tables, execute_sql

def create_lottery_address_summary() -> None:
    execute_sql(
        lottery_engine,
        '''
        DROP TABLE IF EXISTS address_lottery_win_summary;

        CREATE TABLE address_lottery_win_summary AS
        SELECT
            LEFT("지역", 2) AS Big_region,
            SUM("자동당첨건수") AS Total_auto_count
        FROM lottery_win
        GROUP BY LEFT("지역",2);
        '''
    )

def run_batch_processing() -> None:
    print('[batch] 필수 입력 테이블 확인')
    check_required_tables()
    create_lottery_address_summary()
    print('[batch] 배치 처리 완료')


if __name__ =='__main__':
    run_batch_processing()