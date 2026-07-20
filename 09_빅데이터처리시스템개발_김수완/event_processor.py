# ================================================================================
# steam_games/event_processor.py
#   - "이벤트 처리(Event Processing / CEP)" 예제
#       원본 데이터를 대상으로 "이상 상황(조건을 만족하는 사건)"을
#       탐지하여 별도의 알림(alert) 테이블에 기록한다.
#
#   - 이벤트 규칙 : HIGH_METACRITIC_SCORE
#       games.metacritic_score(메타크리틱 점수)가 임계값(threshold)을 "초과"하면
#       고평가 게임 이벤트로 판정한다.
#
#   - 실무의 CEP(Complex Event Processing) 엔진(Esper, Flink CEP 등)은 이런 규칙을
#     스트림에 실시간으로 적용하지만, 여기서는 SQL의 WHERE 조건으로 같은 개념을 단순화
# ================================================================================
import argparse  # 파이썬 프로그램을 실행할 때 터미널에서 전달한 옵션을 읽는 표준 라이브러리
from datetime import datetime

from sqlalchemy import text

from config import METACRITIC_THRESHOLD
from database import engine, check_required_tables, execute_sql


def init_event_alert_table() -> None:
    """
    게임 이벤트 알림을 저장할 테이블을 준비(없으면 생성)

    컬럼 설명:
        event_type      : 이벤트 종류
        app_id          : 어떤 게임에서 발생했는지 (games.app_id)
        game_name       : 게임 이름
        metric_value    : 실제 측정된 값(metacritic_score)
        threshold_value : 이벤트로 판정된 기준값(임계값)
        detected_at     : 언제 이 이벤트가 탐지되었는지
    """
    execute_sql(
        engine,
        """
        CREATE TABLE IF NOT EXISTS event_game_alerts (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            app_id INTEGER NOT NULL,
            game_name VARCHAR(500) NOT NULL,
            metric_value INTEGER NOT NULL,
            threshold_value INTEGER NOT NULL,
            detected_at TIMESTAMP NOT NULL
        );
        """
    )


def detect_high_metacritic_games(threshold: int) -> None:
    """
    games.metacritic_score가 threshold(임계값)를 초과하는 행을 찾아
    "고평가 게임 이벤트"로 등록한다.

    같은 event_type을 먼저 지워서(DELETE) 재실행해도 중복이 쌓이지 않게 한다. (멱등성)
    """
    execute_sql(
        engine,
        """
        DELETE FROM event_game_alerts
        WHERE event_type = 'HIGH_METACRITIC_SCORE';
        """
    )
    execute_sql(
        engine,
        """
        INSERT INTO event_game_alerts(
            event_type, app_id, game_name,
            metric_value,
            threshold_value,
            detected_at
        )
        SELECT
            'HIGH_METACRITIC_SCORE', app_id, name,
            metacritic_score,
            :threshold,       -- 저장할 임계값 자리: 아래 params["threshold"]와 연결
            :detected_at      -- 탐지 시각 자리: 아래 params["detected_at"]와 연결
        FROM games
        WHERE metacritic_score > :threshold;
        """,
        {"threshold": threshold, "detected_at": datetime.now()}
    )
    print(f'[event] 메타크리틱 고평가 이벤트 탐지 완료 threshold={threshold}')


def run_event_processing(metacritic_threshold: int = METACRITIC_THRESHOLD) -> None:
    """이벤트 처리 전체 흐름을 실행하는 엔트리포인트 함수"""
    check_required_tables()               # 원본 테이블 준비 여부 확인
    init_event_alert_table()              # 이벤트 알림 테이블 생성
    detect_high_metacritic_games(metacritic_threshold)  # 고평가 게임 이벤트 탐지
    print('[event] 이벤트 처리 완료')


def parse_args() -> argparse.Namespace:
    """
    argparse 라이브러리를 이용해 커맨드라인 인자를 처리하는 함수

    예) python event_processor.py --metacritic-threshold 90
    -> 임계값을 90점으로 올려서 더 엄격하게 고평가 게임을 탐지하도록 실행

    # ArgumentParser 객체 생성
    ArgumentParser(description='설명글')
    --help 실행 시 상단에 표시되는 설명 문구

    # --metacritic-threshold 옵션 등록
    .add_argument() 함수 : 옵션값, 자료형(타입), 디폴트값(기본값) 설정
    """
    parser = argparse.ArgumentParser(description='게임 데이터 이벤트 처리')

    # type을 설정하지 않으면 기본값이 문자열
    parser.add_argument('--metacritic-threshold', type=int, default=METACRITIC_THRESHOLD)

    return parser.parse_args()  # 실제 실행 시 입력된 값을 읽어서 객체로 변환


if __name__ == '__main__':
    args = parse_args()
    run_event_processing(metacritic_threshold=args.metacritic_threshold)
