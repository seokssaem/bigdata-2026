'''
Food / database.py
-----------------------------
예광탄 방식을 활용한 아주 얇은 코드
DB 연결 - PostgreSQL
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/Food'

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()