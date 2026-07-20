# ===============================================================================
# steam_games/database.py
#   - DB 연결(Engine) 생성과 여러 모듈에서 공통으로 사용하는 DB 유틸리티 함수를 정의
#
# ===============================================================================
from sqlalchemy import create_engine, text

from config import DB_URL

# ------------------------------------------------------------------------------
# DB Engine 생성
#
# echo=False : 실행되는 SQL을 콘솔에 출력하지 않는다(디버깅 시 True로 바꾸면 유용)
# future=True : SQLAlchemy 2.0 스타일 API를 사용하겠다는 의미
# ------------------------------------------------------------------------------
engine = create_engine(DB_URL, echo=False, future=True)


def table_count(engine, table_name: str) -> int:
    """
    주어진 테이블의 전체 행(row) 개수를 반환

    주의: 매개변수 table_name이 사용자 입력값이라면 위험할 수 있다.
            실무에서는 체크를 좀 더 해야 한다.
            반드시 신뢰할 수 있는 값에만 사용해야 한다.
    """
    with engine.connect() as conn:
        # scalar_one() : 결과가 정확히 1행 1열일 때, 그 값 하나만 꺼내는 메서드
        return conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar_one()


def check_required_tables() -> None:
    """
    배치/이벤트 처리를 시작하기 전에, 반드시 존재해야 하는 원본 테이블(games, game_genres)이
    실제로 존재하고 데이터가 들어있는지 점검하는 함수

    "Fail Fast" 원칙
        원본 데이터가 없는 상태로 처리 로직을 실행하면 이해하기 어려운 에러가 한참 뒤에 발생
        미리 검증해서 명확하게 문제 해결
    """
    checks = [
        (engine, 'games', '저장시스템(steam_games) 실습 결과가 필요합니다.'),
        (engine, 'game_genres', '저장시스템(steam_games) 실습 결과가 필요합니다.'),
    ]
    for eng, table_name, hint in checks:
        try:
            count = table_count(eng, table_name)
        except Exception as exc:
            # 테이블 자체가 없거나, DB 접속이 안되는 경우 (원인 exc를 함께 보존)
            raise RuntimeError(f'{table_name} 테이블을 확인할 수 없습니다. {hint} 원인: {exc}') from exc
        if count == 0:
            # 테이블은 있지만 적재된 행이 0건인 경우 (저장시스템 실습 미완료 가능성)
            raise RuntimeError(f'{table_name} 테이블은 존재하지만 데이터가 없습니다. 저장시스템 적재를 먼저 확인하세요.')


def execute_sql(engine, sql: str, params: dict | None = None) -> None:
    """
    여러 문장으로 이루어진 SQL 스크립트(세미콜론으로 구분)를 한번에 실행한다.

    동작 방식:
        1) engine.begin() : 트랜잭션을 시작하고, with 블록이 정상 종료되면
                            자동으로 COMMIT, 예외가 발생하면 자동으로 ROLLBACK
        2) sql.split(';') : SQL 문자열을 세미콜론 기준으로 나눠 여러 statement로 분리
        3) 빈 문자열(공백만 있는 조각)은 제거하고, 각 statement를 순서대로 실행
    """
    with engine.begin() as conn:
        statements = [statement.strip() for statement in sql.split(';') if statement.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})

# ------------------------------------------------------------
# 트랜잭션(Transaction)
#   - 여러 개의 데이터베이스 작업을 하나의 작업 묶음으로 처리하는 것
#   - 묶음 안의 작업이 모두 성공하면 저장하고, 하나라도 실패하면 전부 취소
#
#   모두 성공 -> COMMIT (작업 결과를 최종 저장)
#   하나라도 실패 -> ROLLBACK (작업 시작 전 상태로 되돌린다.)
