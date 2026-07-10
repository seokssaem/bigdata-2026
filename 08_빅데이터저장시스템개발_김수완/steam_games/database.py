# ========================================================
# steam_games/database.py
#
# PostgreSQL 연결 및 세션 관리
# (DB명 : gamesdb, 필요에 맞게 DB_URL 수정해서 사용)
# ========================================================

# 라이브러리 불러오기
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# DB URL 연결 (본인 PostgreSQL 설정에 맞게 계정/비밀번호/포트/DB명 수정)
DB_URL = 'postgresql://postgres:1234@localhost:5432/gamesdb'

# PostgreSQL과 연결할 엔진 생성
# echo=False --> 실행되는 SQL 쿼리 로그를 콘솔에 출력하지 않는다. (디버깅 시에는 True로 변경)
engine = create_engine(DB_URL, echo=False)

# 세션 팩토리 생성
# autoflush=False --> 쿼리 실행 전 자동으로 flush(임시반영) 하지 않는다.
# autocommit=False --> 자동으로 commit()되지 않게, 명시적 commit()을 호출해야 반영된다.
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def init_db(drop_existing: bool = True):
    """
    games 및 자식 테이블들을 초기화(준비)하는 함수

    매개변수(파라미터)
    drop_existing : bool, 기본값 True
        True  --> 기존 테이블을 먼저 삭제하고 새로 만든다.(완전 재설계)
        False --> 기존 테이블이 있으면 그대로 두고, 없을 때만 새로 만든다.
    """
    if drop_existing:
        # 자식 테이블(FK)이 부모보다 먼저 삭제되어야 하므로 metadata가 순서를 자동 처리
        Base.metadata.drop_all(bind=engine)
        print('[database] 기존 테이블 삭제(재설계를 위해)')

    Base.metadata.create_all(bind=engine)
    print('[database] games 및 자식 테이블 준비 완료(기본키 + UNIQUE/FK 제약 적용)')


def get_session():
    """
    Game 등 모델을 다루기 위한 새로운 세션(session)을 하나 생성해서 반환
    """
    return SessionLocal()
