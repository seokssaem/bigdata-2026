from sqlalchemy import create_engine, text
from config import AIRPORT_DB_URL

airport_engine = create_engine(AIRPORT_DB_URL, echo=False, future=True)

def table_count(engine, table_name: str) -> int:
    with engine.connect() as conn:
        return conn.execute(text(f'SELECT COUNT(*) FROM {table_name}')).scalar_one()

def execute_sql(engine, sql: str, params: dict | None = None) -> None:
    with engine.begin() as conn:
        statements = [stmt.strip() for stmt in sql.split(';') if stmt.strip()]
        for statement in statements:
            conn.execute(text(statement), params or {})