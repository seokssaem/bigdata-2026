# ==================================================================
# database/orm.py
#   역할 : 모든 ORM 모델(테이블 클래스)의 부모가 되는 Base 클래스 정의
#
# ORM (Object Relational Mapping)이란?
#   - SQL을 직접 작성하지 않고, python 클래스로 db 테이블을 다루는 방식
#   - 예 : Todo 클래스 -> todo 테이블 자동 생성
# ==================================================================
from sqlalchemy.orm import DeclarativeBase

# Base 클래스 : 이 클래스를 상속받는 모든 클래스는 데이터베이스 테이블로
#               취급한다는 기준점 역할
class Base(DeclarativeBase):
    pass