import argparse
from datetime import datetime
from sqlalchemy import text
from database import apt_engine, check_required_table, execute_sql

def init_price_alert_table() -> None:
    """가격 이상치 이벤트 알림을 저장할 테이블 준비"""
    execute_sql(
        apt_engine,
        '''
        CREATE TABLE IF NOT EXISTS apt_price_event_alerts (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            law_dong VARCHAR(10) NOT NULL,
            apt_name VARCHAR(100) NOT NULL,
            price_per_area NUMERIC(20,1) NOT NULL,
            avg_dong_price NUMERIC(20,2) NOT NULL,
            multiplier_value NUMERIC(4,2) NOT NULL,
            detected_at TIMESTAMP NOT NULL
        );
        '''
    )

def check_dong_summary_ready() -> None:
    """apt_dong_summary 테이블 존재 확인"""
    try:
        with apt_engine.connect() as conn:
            conn.execute(text('SELECT 1 FROM apt_dong_summary LIMIT 1'))
        print('배치 처리 결과 테이블 확인 완료: apt_dong_summary')
    except Exception as exc:
        raise RuntimeError(
            'apt_dong_summary 테이블이 없습니다.'
            '배치 처리를 먼저 실행하십시오.'
        ) from exc

def detect_price_outliers(multiplier: float) -> None:
    """
    평당가격(price_per_area)이 법정동별 평균값(avg_price_per_area)에 대해
    (평균값 * multiplier) 이상이거나 (평균값 / multiplier) 이하인 행을 찾아
    "가격 이상치(PRICE_OUTLIERS)"로 등록
    """
    execute_sql(
        apt_engine,
        """
        DELETE FROM apt_price_event_alerts
        WHERE event_type = 'PRICE_OUTLIERS';
        """
    )
    execute_sql(
        apt_engine,
        """
        INSERT INTO apt_price_event_alerts(
            event_type, law_dong, apt_name,
            price_per_area, avg_dong_price,
            multiplier_value,
            detected_at
        )
        SELECT
            'PRICE_OUTLIERS', d."법정동", d."단지명",
            d."평당가격", s.avg_price_per_area,
            :multiplier,
            :detected_at
        FROM apt_deal d
        JOIN apt_dong_summary s
            ON d."법정동" = s.law_dong
        WHERE d."평당가격" >= (s.avg_price_per_area * :multiplier)
            OR d."평당가격" <= (s.avg_price_per_area / :multiplier);
        """,
        {"multiplier":multiplier, "detected_at":datetime.now()}
    )
    print(f'[event] 가격 이상치 이벤트 탐지 완료 multiplier={multiplier}')

def parse_args() -> argparse.Namespace:
    """커맨드라인 인자 처리"""
    parser = argparse.ArgumentParser(description='아파트 실거래가 데이터 이벤트 처리')
    parser.add_argument('--price-multiplier', type=float, default=1.5)
    return parser.parse_args()

def run_event_processing(price_multiplier: float=1.5) -> None:
    """이벤트 처리 실행"""
    print('[event] 필수 테이블 확인')
    check_required_table()
    check_dong_summary_ready()
    init_price_alert_table()
    detect_price_outliers(price_multiplier)
    print('[event] 이벤트 처리 완료')