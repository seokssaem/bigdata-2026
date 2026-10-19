"""
내 컴퓨터 DB의 가격 데이터를 initdb/price_report.sql 한 파일로 내보낸다.

왜 필요한가?
  서버(Docker)의 DB는 처음에는 텅 비어 있다. 원본 CSV(수백 MB)를 서버에 올려서 다시 계산하는 대신,
  이미 계산이 끝난 결과(상품, 가격이력, 등락률, 예측)만 SQL 파일로 뽑아서 서버 DB에 그대로 넣는다.
  docker-compose.yml 이 initdb 폴더의 .sql 파일을 DB가 처음 만들어질 때 자동으로 실행해 준다.

내보내는 것: products, price_history, price_changes, predictions  (회원 정보 users/favorites 는 제외)

실행 (프로젝트 폴더에서):  uv run python export_db_sql.py
"""
import os
from datetime import date, datetime

from sqlalchemy import select
from sqlalchemy.dialects import postgresql
from sqlalchemy.schema import CreateIndex, CreateTable

from database import engine
import models

OUTPUT_PATH = "initdb/price_report.sql"

# 순서가 중요하다: products 를 먼저 만들어야 나머지가 product_id 로 참조할 수 있다
TABLES = [
    models.Product.__table__,
    models.PriceHistory.__table__,
    models.PriceChange.__table__,
    models.Prediction.__table__,
]


def to_copy_value(value) -> str:
    """값 하나를 PostgreSQL COPY(탭으로 구분한 텍스트) 형식의 글자로 바꾼다."""
    if value is None:
        return r"\N"                      # NULL
    if isinstance(value, float):
        if value != value:                # NaN 이 들어 있어도 NULL(값 없음)로 바꿔서 내보낸다
            return r"\N"
        return repr(value)
    if isinstance(value, (datetime, date)):
        return value.isoformat(sep=" ") if isinstance(value, datetime) else value.isoformat()
    # 문자열: 줄바꿈/탭/역슬래시는 COPY 형식에서 특별한 뜻이라서 이스케이프한다
    return (str(value)
            .replace("\\", "\\\\")
            .replace("\t", "\\t")
            .replace("\n", "\\n")
            .replace("\r", "\\r"))


def main():
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    dialect = postgresql.dialect()
    counts = {}

    with engine.connect() as conn, open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as out:
        out.write("-- 생필품 가격 리포트: 가격 데이터 (export_db_sql.py 로 자동 생성한 파일, 직접 고치지 않는다)\n")
        out.write("SET client_encoding = 'UTF8';\n\n")

        for table in TABLES:
            rows = conn.execute(select(table).order_by(table.c.id)).all()
            counts[table.name] = len(rows)

            # 1) 테이블 만들기 (이미 있으면 건너뜀)
            out.write(str(CreateTable(table, if_not_exists=True).compile(dialect=dialect)).strip() + ";\n")
            for index in table.indexes:
                out.write(str(CreateIndex(index, if_not_exists=True).compile(dialect=dialect)).strip() + ";\n")

            # 2) 데이터 넣기 (COPY: 한 번에 대량으로 넣는 가장 빠른 방법)
            columns = [c.name for c in table.columns]
            out.write(f"\nCOPY {table.name} ({', '.join(columns)}) FROM stdin;\n")
            for row in rows:
                out.write("\t".join(to_copy_value(v) for v in row) + "\n")
            out.write("\\.\n\n")

            # 3) id 자동번호가 이어서 매겨지도록 맞춰두기
            out.write(
                f"SELECT setval(pg_get_serial_sequence('{table.name}', 'id'), "
                f"COALESCE((SELECT MAX(id) FROM {table.name}), 1));\n\n"
            )

    for name, n in counts.items():
        print(f"{name}: {n}행")
    if counts.get("products", 0) == 0:
        print("경고: products 가 비어 있습니다. 먼저 'uv run python -m services.load_to_db' 로 데이터를 적재하세요.")
    size_mb = os.path.getsize(OUTPUT_PATH) / 1024 / 1024
    print(f"완료: {OUTPUT_PATH} ({size_mb:.1f} MB)")


if __name__ == "__main__":
    main()
