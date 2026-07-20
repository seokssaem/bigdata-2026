# =================================================================================================
# 09_빅데이터처리시스템개발_김동욱/event_processor.py
#     - 이벤트 처리 : 잔류염소 0.74초과
# =================================================================================================
import argparse
from datetime import datetime

from config import RESIDUAL_CHLORINE_MAX
from database import water_engine, check_required_tables, execute_sql

def init_water_event_table() -> None:
    """
    잔류염소가 0.74 초과인 정수장별 구분별 수질검사 결과를 저장할 테이블 준비

    컬럼 설명 :
        event_type       : 이벤트 종류
        정수장           : 정수장 이름
        구분             : 정수1 / 정수2 구분
        ph               : ph농도 측정값
        탁도             : 탁도 측정값
        잔류염소         : 잔류염소 측정값
        검사시기         : 수질검사 시기
        잔류염소_기준값   : 이벤트 판정 기준값(잔류염소 0.74초과)
        이벤트_시간       : 이벤트 탐지 시간
    """
    execute_sql(
        water_engine,
        """
        CREATE TABLE IF NOT EXISTS event_water_chlorine_alert (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            정수장 VARCHAR(10) NOT NULL,
            구분 VARCHAR(10) NOT NULL,
            ph NUMERIC(5,2) NOT NULL,
            탁도 NUMERIC(5,2) NOT NULL,
            잔류염소 NUMERIC(5,2) NOT NULL,
            검사시기 DATE NOT NULL,
            잔류염소_기준값 NUMERIC(5,2) NOT NULL,
            이벤트_시간 TIMESTAMP NOT NULL
        );
        """
    )

def detect_water_event(threshold: float) -> None:
    """수질검사 결과 테이블에서 잔류염소가 0.74(threshold : 임계값) 초과인 행을 찾아 이벤트로 등록"""
    execute_sql(
        water_engine,
        """
        DELETE FROM event_water_chlorine_alert
        WHERE event_type = 'WATER_EVENT';

        """
    )
    execute_sql(
        water_engine,
        """
        INSERT INTO event_water_chlorine_alert(
            event_type, 정수장, 구분, ph, 탁도, 잔류염소, 검사시기,
            잔류염소_기준값, 이벤트_시간
        )
        SELECT
            'WATER_EVENT', 정수장, 구분, ph, 탁도, 잔류염소, 검사시기,
            :threshold,
            :detected_at
        FROM water
        WHERE 잔류염소 > :threshold;

        """,
        {"threshold": threshold, "detected_at": datetime.now()}
    )
    print(f'[event] 잔류염소 이벤트 탐지 완료 : event_water_chlorine_alert (잔류염소 > {threshold})')

def run_event_processing(water_threshold: float = 0.74) -> None:
    """이벤트 처리 전체 흐름을 실행하는 엔트리포인트 함수"""

    check_required_tables()
    init_water_event_table()
    detect_water_event(water_threshold)
    print("[event] 이벤트 처리 완료")


def parse_args() -> argparse.Namespace:
    """argparse 라이브러리를 이용해 커맨드라인 인자를 처리하는 함수"""

    parser = argparse.ArgumentParser(description="수질검사 이벤트 처리")

    parser.add_argument("--water-threshold", type=float, default=RESIDUAL_CHLORINE_MAX)

    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    run_event_processing(water_threshold=args.water_threshold)
