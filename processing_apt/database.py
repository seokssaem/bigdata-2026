from sqlalchemy import create_engine, text
from config import DB_URL

apt_engine = create_engine(DB_URL, echo=False, future=True)

def table_count(engine, table_name: str) -> int:
    """테이블의 전체 행 개수 반환"""
    with engine.connect() as conn:
        return conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar_one()
    
def check_required_table() -> None:
    """필요한 테이블 존재 확인"""
    checks = [(apt_engine, 'apt_deal', '아파트 실거래가 저장시스템 실습 결과가 필요합니다.')]

    for engine, table_name, hint in checks:
        try:
            count = table_count(engine, table_name)
            print(f'입력 테이블 확인 완료: {table_name} {count:,}건')
        except Exception as exc:
            raise RuntimeError(f'{table_name} 테이블을 확인할 수 없습니다. {hint} 원인 : {exc}') from exc
        if count == 0:
            raise RuntimeError(f'{table_name} 테이블은 존재하지만 데이터가 없습니다.')
        
def execute_sql(engine, sql: str, params: dict | None=None):
    """SQL 문장 실행"""
    with engine.begin() as conn:
        statements = [statement.strip() for statement in sql.split(';') if statement.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})