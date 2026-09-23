from sqlalchemy import create_engine, text

from config import LOTTERAPI_DB_URL

lottery_engine = create_engine(LOTTERAPI_DB_URL, echo=False, future=True)

def table_count(engine, table_name: str) -> int:
    with engine.connect() as conn:
        return conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar_one()
    
def check_required_tables() -> None:
    checks = [(lottery_engine, "lottery_win", "로또 저장 시스템 실습 결과가 필요합니다.")]

    for engine, table_name, hint in checks:
        try:
            count = table_count(engine, table_name)
        except Exception as exc:
            raise RuntimeError(f'{table_name} 테이블을 확인할 수 없습니다. {hint} 원인: {exc}') from exc
        if count == 0:
            raise RuntimeError(f'{table_name} 테이블에 저장된 데이터가 없습니다.')
        
def execute_sql(engine, sql:str, params:dict | None = None) -> None:
    with engine.begin() as conn:
        statements = [statement.strip() for statement in sql.split(';') if statement.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})