# ====================================================
# 기술은행 수요기술 조회 서비스/database.py
# ====================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from models import Base

DB_URL = 'postgresql://postgres:1234@localhost:5432/NTBdb'

# PostgreSQL과 연결할 엔진 생성ㅌ
engine = create_engine(DB_URL, echo=False) 

# 세션 팩토리 생성
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

# 테이블 재설계 함수 정의
def init_db(drop_existing: bool = True):
    """
    매개변수(파라미터)
    drop_existing : bool, 기본값 True
        True --> 기존 테이블을 먼저 삭제하고 새로 만든다.(완전 재설계)
        False --> 기존 테이블이 있으면 그대로 두고, 없을 때만 새로 만든다.

    """
    if drop_existing:
        Base.metadata.drop_all(bind=engine)
        print('[database] 기존 tech 테이블 삭제(재설계를 위해)')

    Base.metadata.create_all(bind=engine)
    print('[database] tech 테이블 준비 완료(기본키 + UNIQUE 제약 적용)')

def get_session():
    """
    모델을 다루기 위한 새로운 세션(session)을 하나 생성해서 반환
    실제로 사용 가능한 세션 객체가 생성되도록 한다.
    """
    return SessionLocal()