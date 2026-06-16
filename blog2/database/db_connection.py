# ========================================================================
# database/db_connection.py
#
# 역할 : PostgreSQL DB 연결 설정
#       - 연결 문자열(DATABASE_URL) 정의
#           --> 형식
#               postgresql+psycopg2://유저명:비밀번호@호스트:포트번호/DB이름
#       - 엔진(engine) 생성
#       - 세션 팩토리(SessionFactory) 생성
#           --> 엔진 : 데이터베이스와의 실제 연결을 관리하는 객체
#       - 세션 팩토리(SessionFactory) 생성
#           --> ORM이 데이터베이스와 상호작용할 때 사용하는 작업 단위
#       - 흐름 : 1. 엔진을 생성하고, 그 엔진을 기반으로 세션을 생성한다.
#                2. 세션을 통해 데이터를 생성, 조회, 수정, 삭제하며,
#                   이 과정에서 발생하는 모든 변경 사항을 세션이 관리한다.
# ========================================================================
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg2://postgres:1234@localhost:5432/blogdb'

# 엔진 생성
# echo=True --> 실행되는 SQL을 터미널에 출력(디버깅용)
#               지금 입문시간이여서 수업용으로 확인하는 것 (실제로는 False)
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,   # session.commit()을 직접 호출해야 DB에 반영
    autoflush=False,    # flush : commit전에 SQL을 실행하는 중간 단계
    expire_on_commit=False, # commit 후에도 데이터가 메모리에 유지된다. (TRue라면 db다시 조회)
    bind=engine, # 위에서 만든 엔진과 세션을 연결
)