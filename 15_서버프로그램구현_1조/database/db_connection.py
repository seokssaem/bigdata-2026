'''
database/db_connection.py - PostgreSQL 연결 + 세션 의존성
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# moviedb 데이터베이스가 먼저 생성되어 있어야 함. 계정/비밀번호는 각자 환경에 맞게 수정
DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/moviedb1'

engine = create_engine(DATABASE_URL, echo=True)

SessionFactory = sessionmaker(autocommit=False, autoflush=False, expire_on_commit=False, bind=engine)


def get_session():
    session = SessionFactory()
    try:
        yield session
    finally:
        session.close()
