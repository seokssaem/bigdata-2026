'''
Food / database.py

DB 연결 - PostgreSQL
'''
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/Food"
)

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