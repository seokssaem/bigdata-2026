from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = 'postgresql://postgres:1234@localhost:5432/cafedb'
engine = create_engine(DB_URL, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db(drop_existing: bool = True):
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
        print('[database] 기존 테이블 삭제')
    Base.metadata.create_all(bind=engine)
    print('[database] menu 테이블 준비 완료')

def get_session():
    return SessionLocal()