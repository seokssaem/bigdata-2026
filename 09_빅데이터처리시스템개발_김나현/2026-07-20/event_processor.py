
import argparse  # 파이썬 프로그램을 실행할 때 터미널에서 전달한 옵션을 읽는 표준 라이브러리
from datetime import datetime

from sqlalchemy import text

from database import ntb_engine, check_required_tables, execute_sql

def init_missing_fee_table() -> None:
    """
    기술료 미기재 테이블을 준비(없으면 생성)

    컬럼 설명:
        event_type : 이벤트 종류
        tech_no : 수요기술번호
        tech_name : 수요기술명
        detail : 이벤트 상세 내용
        detected_at : 언제 이 이벤트가 탐지 되었는지
    
    """
    execute_sql(
        ntb_engine,
        """
        CREATE TABLE IF NOT EXISTS missing_fee_event_alerts (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            tech_no VARCHAR(100),
            tech_name VARCHAR(300),
            detail TEXT NOT NULL,
            detected_at TIMESTAMP NOT NULL
        );
        """
    )

def init_low_information_table() -> None:
    """
    기술은행 이벤트 알림을 저장할 테이블을 생성한다.

    컬럼 설명
        event_type : 이벤트 종류
        tech_no : 수요기술번호
        tech_name : 수요기술명
        metric_value : 실제 정보충실도
        threshold_value : 이벤트 판정 기준
        detail : 이벤트 상세 내용
        detected_at : 이벤트 탐지 시각
    """

    execute_sql(
        ntb_engine,
        """
        CREATE TABLE IF NOT EXISTS low_information_event_alerts (
            id BIGSERIAL PRIMARY KEY,
            event_type VARCHAR(50) NOT NULL,
            tech_no VARCHAR(100),
            tech_name VARCHAR(300),
            metric_value INTEGER,
            threshold_value INTEGER,
            detail TEXT,
            detected_at TIMESTAMP NOT NULL
        );
        """
    )


def detect_fee_negotiation_event() -> None:
    """
    기술료가 모두 미기재된 수요기술을 탐지하여 이벤트 테이블에 저장한다.
    """

    # 기존 이벤트 삭제 (멱등성)
    execute_sql(
        ntb_engine,
        """
        DELETE FROM missing_fee_event_alerts
        WHERE event_type = 'TECH_FEE_NEGOTIATION';
        """
    )

    # 이벤트 등록
    execute_sql(
        ntb_engine,
        """
        INSERT INTO missing_fee_event_alerts (
            event_type,
            tech_no,
            tech_name,
            detail,
            detected_at
        )
        SELECT
            'TECH_FEE_NEGOTIATION',
            "수요기술번호",
            "수요기술명",
            '기술료가 협의 후 결정',
            :detected_at
        FROM tech
        WHERE
            정액기술료 = '협의후 결정'
        OR
            경상기술료 = '협의후 결정';
        """,
        {
            "detected_at": datetime.now()
        }
    )

    print("[event] 기술료 미기재 이벤트 탐지 완료")

def detect_low_information_event(threshold: int) -> None:
    """
    정보충실도가 threshold 이하인 기술을 탐지하여 이벤트를 생성한다.

    Parameters
    ----------
    threshold : int
        정보충실도 임계값(기본값: 2)
    """

    # 기존 이벤트 삭제 (멱등성)
    execute_sql(
        ntb_engine,
        """
        DELETE FROM low_information_event_alerts
        WHERE event_type = 'LOW_INFORMATION';
        """
    )

    # 이벤트 생성
    execute_sql(
        ntb_engine,
        """
        INSERT INTO low_information_event_alerts (
            event_type,
            tech_no,
            tech_name,
            metric_value,
            threshold_value,
            detail,
            detected_at
        )
        SELECT
            'LOW_INFORMATION',
            "수요기술번호",
            "수요기술명",
            "정보충실도",
            :threshold,
            '정보충실도가 기준 이하',
            :detected_at
        FROM tech
        WHERE "정보충실도" <= :threshold;
        """,
        {
            "threshold": threshold,
            "detected_at": datetime.now()
        }
    )

    print(f"[event] 정보충실도 부족 이벤트 탐지 완료 (기준={threshold})")

# def check_subway_summary_ready() -> None:
#     """
#     이벤트 처리는 배치 처리 결과(traffic_subway_hourly_summary)를 입력으로 사용하므로
#     이 테이블이 먼저 만들어져야 한다. 실행 순서를 알려주는 함수
#     """
#     try:
#         with ntb_engine.connect() as conn:
#             conn.execute(text("SELECT 1 FROM traffic_subway_hourly_summary LIMIT 1"))

#     except Exception as exc:
#         raise RuntimeError(
#             "traffic_subway_hourly_summary 테이블이 없습니다."
#             "event_processor.py 실행 전에 batch_processor.py를 먼저 실행하세요."
#         ) from exc
    

def run_event_processing(tech_threshold: int = 100000) -> None:
    """이벤트 저리 전체 흐름을 실행하는 엔트리포인트 함수"""
    check_required_tables()  # 원본 테이블 준비 여부 확인
    # check_subway_summary_ready()  # 배치 처리 결과(집계 테이블) 준비 여부 확인

    init_missing_fee_table()  # 기술료 미기재 테이블 생성
    init_low_information_table()  # 정보충실도 미달 테이블 생성

    detect_fee_negotiation_event()  # 기술료 미기재 확인 이벤트
    detect_low_information_event(tech_threshold)  # 정보충실도 미달 확인 이벤트
    print('[event] 이벤트 처리 완료')

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='기술은행 기술목록 데이터 이벤트 처리')

    # type을 설정하지 않으면 기본값이 문자열
    parser.add_argument('--tech-threshold', type=int, default=1)

    return parser.parse_args() # 실제 실행 시 입력된 값을 읽어서 객체로 반환

if __name__ == '__main__':
    args = parse_args()  
    run_event_processing(tech_threshold=args.tech_threshold)