# ========================================================================
# models.py
#
# 역할 : DB 테이블 구조를 Python 클래스로 정의 (ORM 모델)
# 예) 이 파일의 클래스 한 개 == DB 테이블 한 개
#       클래스와 속성 한 개 == 테이블의 컬럼 한 개
# ========================================================================
from sqlalchemy import Integer, String, Boolean # 컬럼 타입 임포트
# Mapped:ORM에 의해 관리되는 컬럼
# mapped_column : 파이썬 클래스의 속성을 데이터베이스 컬럼으로 연결하는 역할
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base

# Post 모델 정의
class Post(Base):
    # DB에서 실제로 사용할 테이블 이름
    __tablename__ = 'post'

    id: Mapped[int] = mapped_column(
        Integer,    # 컬럼 타입 : 정수
        primary_key=True,  # 기본키(각 행을 구분하는 고유번호)
        autoincrement=True, # 자동 증가(1,2,3...)
    )

    title: Mapped[str] = mapped_column(
        String(255), # 컬럼 타입 : 최대 255자 문자열
        nullable=False, # 반드시 값이 있어야 한다.
    )

    content: Mapped[str] = mapped_column(
        String(1000),
        nullable=False,
    )