from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DB_URL = 'postgresql://postgres:1234@localhost:5432/airportdb'
engine = create_engine(DB_URL, echo=False) 

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def init_db():
    Base.metadata.create_all(bind=engine)
    print('[database] airport_congestion 테이블 준비 완료 (복합 기본키 적용)')

def get_session():
    return SessionLocal()

if __name__ == '__main__':
    init_db()