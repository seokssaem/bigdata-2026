# ===================================================================
# database/orm.py
#   역할 : 모든 ORM 모델(테이블 클래스)의 부모가 되는 Base 클래스 정의
# ===================================================================
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
