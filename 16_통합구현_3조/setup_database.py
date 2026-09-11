# =========================================================================
# setup_database.py
#
# =========================================================================
import os
import sys

try:
    import pandas as pd
    from dotenv import load_dotenv
    from sqlalchemy import create_engine, text
except ImportError as e:
    print(f"[오류] 필요한 라이브러리가 설치되어 있지 않습니다: {e}")
    print("먼저 아래 명령으로 라이브러리를 설치해주세요:")
    print("    pip install -r requirements.txt")
    sys.exit(1)

# 이 파일이 있는 폴더를 기준으로 경로를 잡음 (어디서 실행해도 안전하게)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(BASE_DIR, "schema.sql")
DATA_DIR = os.path.join(BASE_DIR, "data")
ENV_PATH = os.path.join(BASE_DIR, ".env")

TABLES = {
    "players": "players.csv",
    "matches": "matches.csv",
    "teams": "teams.csv",
    "playerse": "playersE.csv"
}


def load_database_url() -> str:
    if not os.path.exists(ENV_PATH):
        print("[오류] .env 파일이 없습니다.")
        print("      .env.example을 복사해서 .env를 만들고, DATABASE_URL을")
        print("      본인의 pgAdmin4 접속 정보(사용자명/비밀번호/포트)에 맞게 수정해주세요.")
        sys.exit(1)

    load_dotenv(ENV_PATH)
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("[오류] .env 파일에 DATABASE_URL이 설정되어 있지 않습니다.")
        sys.exit(1)
    return database_url


def run_schema(engine):
    print(f"1) {SCHEMA_PATH} 실행해서 테이블 생성 중...")
    with open(SCHEMA_PATH, encoding="utf-8") as f:
        schema_sql = f.read()

    # 주석 줄 전부 제거
    lines = [
        line for line in schema_sql.splitlines()
        if not line.strip().startswith("--")
    ]
    schema_sql = "\n".join(lines)

    with engine.begin() as conn:
        for statement in schema_sql.split(";"):
            statement = statement.strip()
            if statement and not statement.startswith("--"):
                conn.execute(text(statement))
    print("   -> 완료 (players / matches / teams / playerE 테이블 생성됨)\n")


def load_csv(engine, table: str, filename: str):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        print(f"[오류] {path} 파일을 찾을 수 없습니다.")
        sys.exit(1)

    try:
        df = pd.read_csv(path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(path, encoding="cp949")

    df.to_sql(table, engine, if_exists="append", index=False)
    print(f"   -> {filename} 를 {table} 테이블에 {len(df)}행 적재 완료")


def main():
    print("=" * 60)
    print("2026 FIFA 월드컵 데이터베이스 세팅을 시작합니다")
    print("=" * 60)

    database_url = load_database_url()

    try:
        engine = create_engine(database_url)
        with engine.connect():
            pass  # 접속만 확인
    except Exception as e:
        print(f"[오류] 데이터베이스 접속에 실패했습니다: {e}")
        print("      pgAdmin4에서 worldcup 데이터베이스가 실제로 만들어져 있는지,")
        print("      .env의 DATABASE_URL(사용자명/비밀번호/포트)이 맞는지 확인해주세요.")
        sys.exit(1)

    run_schema(engine)

    for table, filename in TABLES.items():
        load_csv(engine, table, filename)


if __name__ == "__main__":
    main()