'''
database/db_connection.py - PostgreSQL 연결 + 세션 의존성
'''
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

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