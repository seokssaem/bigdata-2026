"""
데이터베이스 연결 설정

.env 파일(또는 환경변수)의 DATABASE_URL을 읽어서 사용한다.
.env가 없으면 로컬 개발용 기본값을 사용한다.
FastAPI 엔드포인트에서는 Depends(get_db)로 세션을 주입받아 사용한다.
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()  # .env 파일을 읽어서 환경변수로 등록

def normalize_database_url(url: str) -> str:
    """주소 앞부분(postgres:// 또는 postgresql://)을 'postgresql+psycopg2://' 로 통일한다.

    SQLAlchemy 최신 버전은 'postgresql://' 만 적혀 있으면 psycopg(3)를 찾는데,
    이 프로젝트는 psycopg2-binary 를 쓰기 때문에 드라이버를 직접 지정해 준다.
    (배포 서비스가 'postgres://' 로 시작하는 주소를 주는 경우도 같이 처리한다)
    sqlite 처럼 다른 DB 주소는 그대로 둔다.
    """
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg2://" + url[len(prefix):]
    return url


DATABASE_URL = normalize_database_url(os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/price_report",
))

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """FastAPI 의존성 주입용 - 요청마다 세션을 열고 끝나면 닫는다."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()