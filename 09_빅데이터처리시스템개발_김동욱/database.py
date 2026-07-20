# ===========================================================================
# 09_빅데이터처리시스템개발_김동욱/database.py
#     - engine 생성 및 공통 유틸리티
# ===========================================================================
from sqlalchemy import create_engine, text

from config import WATER_DB_URL

water_engine = create_engine(WATER_DB_URL, echo=False, future=True)

def table_count(engine, table_name: str) -> int:
    """
    주어진 테이블의 전체 행(row) 개수를 반환
    """
    with engine.connect() as conn:
        return conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).scalar_one()
    
def check_required_tables() -> None:
    """
    원본 테이블(water)이 실제로 존재하고 데이터가 들어있는지 점검하는 함수.
    """
    checks = [
        (water_engine, "water", "정수장 수질검사 결과 테이블이 필요합니다."),
    ]
    for engine, table_name, hint in checks:
        try:
            count = table_count(engine, table_name)
        except Exception as exc:
            raise RuntimeError(f"{table_name} 테이블을 확인할 수 없습니다.\n{hint}\n원인 : {exc}") from exc
        if count == 0:
            raise RuntimeError(f"{table_name} 테이블은 존재하지만 데이터가 없습니다.")

def execute_sql(engine, sql: str, params: dict | None = None) -> None:
    """
    여러 문장으로 이루어진 SQL 스크립트(세미 콜론으로 구분)를 한번에 실행
    """
    with engine.begin() as conn:
        statements = [statement.strip() for statement in sql.split(";") if statement.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})