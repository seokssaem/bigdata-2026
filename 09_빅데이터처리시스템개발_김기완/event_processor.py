from datetime import datetime
from sqlalchemy import text
from config import CONGESTION_THRESHOLD
from database import airport_engine, execute_sql

def init_airport_alert_table() -> None:
    execute_sql(
        airport_engine,
        """
        CREATE TABLE IF NOT EXISTS traffic_airport_event_alerts (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            airport_code VARCHAR(10) NOT NULL,
            collect_hour VARCHAR(10) NOT NULL,
            metric_value NUMERIC(5,2) NOT NULL,
            threshold_value NUMERIC(5,2) NOT NULL,
            detected_at TIMESTAMP NOT NULL
        );
        """
    )

def check_input_table_ready() -> None:
    try:
        with airport_engine.connect() as conn:
            conn.execute(text("SELECT 1 FROM airport_congestion LIMIT 1"))
    except Exception as exc:
        raise RuntimeError("입력 데이터가 없습니다. 저장시스템 테이블을 확인하세요.") from exc

def detect_high_congestion(threshold: float) -> None:
    execute_sql(
        airport_engine,
        """
        DELETE FROM traffic_airport_event_alerts WHERE event_type = 'AIRPORT_HIGH_CONGESTION';

        INSERT INTO traffic_airport_event_alerts (
            event_type, airport_code, collect_hour, metric_value, threshold_value, detected_at
        )
        SELECT
            'AIRPORT_HIGH_CONGESTION', "공항코드", "수집시간", "전체_혼잡도", :threshold, :detected_at
        FROM airport_congestion
        WHERE "전체_혼잡도" >= :threshold;
        """,
        {"threshold": threshold, "detected_at": datetime.now()}
    )
    print(f'[event] 숫자형 기준 혼잡 이벤트 탐지 완료 threshold={threshold}')

def main() -> None:
    print('[event] 이벤트 처리 시작')
    check_input_table_ready()
    init_airport_alert_table()
    detect_high_congestion(CONGESTION_THRESHOLD)
    print('[event] 이벤트 처리 완료')

if __name__ == '__main__':
    main()