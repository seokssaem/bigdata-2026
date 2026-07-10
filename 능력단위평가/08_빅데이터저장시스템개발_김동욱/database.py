# ================================================
# TEST/08_빅데이터저장시스템개발_김동욱/database.py
#
# PostgreSQL 연결 및 세션 관리
# (DB명: water_DB, 비밀번호: 1234)
# ================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = "postgresql://postgres:1234@localhost:5432/water_DB"

engine = create_engine(DB_URL, echo=False) 

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    print("water, area 테이블 준비 완료")

def get_session():
    return SessionLocal()

if __name__ == "__main__":
    init_db()