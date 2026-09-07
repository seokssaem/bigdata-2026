'''
database/db_connection.py - PostgreSQL 연결 + 세션 의존성
'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# 환경변수 DATABASE_URL이 있으면 그 값을 사용하고(도커 환경),
# 없으면 기존처럼 localhost 기준 값을 사용한다(로컬 개발 환경, 기존 동작 그대로 유지).
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg2://postgres:1234@localhost:5432/moviedb1',
)

engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
