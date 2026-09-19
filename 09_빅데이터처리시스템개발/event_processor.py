from datetime import datetime
from sqlalchemy import text
from config import lottery_win_min, lottery_win_max, lottery_address
from database import lottery_engine, check_required_tables, execute_sql

def init_lottery_alert_table() -> None:
    execute_sql(
        lottery_engine,
        """
        CREATE TABLE IF NOT EXISTS address_lottery_event_alerts(
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,    
            store_name VARCHAR(300) NOT NULL,
            store_reigon VARCHAR(300) NOT NULL,
            metric_value INTEGER NOT NULL,
            detail TEXT NOT NULL,
            detected_at TIMESTAMP NOT NULL
        )
        """
)


def lottery_event_table() -> None:
    execute_sql(lottery_engine, "DELETE FROM address_lottery_event_alerts;")
    execute_sql(
        lottery_engine,
        """
        INSERT INTO address_lottery_event_alerts(
            event_type, store_name, store_reigon, metric_value,detail, detected_at
        )
        SELECT
            'WIN_COUNT_IN_OF_RANGE', "상호", "지역", "자동당첨건수", 
            CONCAT('WIN=', "자동당첨건수"),
            :detected_at
        FROM lottery_win
        WHERE "자동당첨건수" IS NOT NULL
            AND "자동당첨건수" BETWEEN :win_min AND :win_max
        """,
        {
            "win_min": lottery_win_min,
            "win_max": lottery_win_max,
            "detected_at" : datetime.now()
        }
    )

    allowed_values = ', '.join(f"'{value}'" for value in sorted(lottery_address))
    execute_sql(
        lottery_engine,
        f"""
        INSERT INTO address_lottery_event_alerts(
            event_type, store_name, store_reigon, metric_value,detail, detected_at
        )
        SELECT 
            'LOTTERY_LOCATION_GROUP', "상호", "지역", "자동당첨건수",
            CONCAT('location_group=', COALESCE("지역", 'NULL')),
            :detected_at
        FROM lottery_win
        WHERE LEFT("지역",2) IN ({allowed_values});
        """,
        {"detected_at": datetime.now()}
    )
    print('[event] 당첨 횟수/지역 이벤트 탐지 완료')

def run_event_processing() -> None:
    check_required_tables()
    init_lottery_alert_table()
    lottery_event_table()
    print('[event]이벤트 처리 완료')


if __name__ == '__main__':
    run_event_processing()
    