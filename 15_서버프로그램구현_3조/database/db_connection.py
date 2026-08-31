# ===========================================================================
# database/db_connection.py
#
# 역할 : PostgreSQL DB 연결 설정
#       - 연결 문자열(DATABASE_URL) 정의
#           --> 형식
#               postgresql+psycopg2://유저명:비밀번호@호스트:포트번호/DB이름
#       - 엔진(engine) 생성
#           --> 엔진 : 데이터베이스와의 실제 연결을 관리하는 객체
#       - 세션 팩토리(SessionFactory) 생성
#           --> ORM이 데이터베이스와 상호작용할 때 사용하는 작업 단위
# ===========================================================================
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()  # .env 파일이 있으면 환경변수로 읽어들임

# 환경변수(DATABASE_URL)가 있으면 그걸 쓰고, 없으면 로컬 기본값 사용
DATABASE_URL = os.getenv(
    'DATABASE_URL',
    'postgresql+psycopg2://postgres:1234@localhost:5432/worldcup',
)

# 엔진 생성
# echo=True --> 실행되는 SQL을 터미널에 출력(디버깅용). 필요 없으면 False로 바꿔도 됨
engine = create_engine(DATABASE_URL, echo=True)

# 세션 팩토리 생성
SessionFactory = sessionmaker(
    autocommit=False,   # session.commit()을 직접 호출해야 DB에 반영
    autoflush=False,    # flush : commit 전에 SQL을 실행하는 중간 단계
    expire_on_commit=False,  # commit 후에도 데이터가 메모리에 유지된다.
    bind=engine,         # 위에서 만든 엔진과 세션을 연결
)
