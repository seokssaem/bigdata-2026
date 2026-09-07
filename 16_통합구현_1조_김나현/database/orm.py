'''
database/orm.py - 모든 ORM 모델의 부모 Base 클래스
'''
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
