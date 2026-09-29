# ==============================================================
# models.py
# - SQLAlchemy ORM 모델 정의 파일
# - 파이썬 클래스 ↔ DB 테이블 --> 매핑(mapping)하는 부분
# ==============================================================
from sqlalchemy import Integer, Numeric, String, Date, Time
from sqlalchemy.orm import Mapped, mapped_column
from database.orm import Base


# --- Player 모델 (선수 테이블) -----------------------------
class Player(Base):
    __tablename__ = 'players'  # 실제 DB 테이블 이름

    # DB 컬럼명은 players_id 인데, 파이썬에서는 짧게 id로 쓰고 싶어서
    # mapped_column('players_id', ...) 처럼 컬럼명을 직접 지정
    id: Mapped[int] = mapped_column('players_id', Integer, primary_key=True)

    player: Mapped[str | None] = mapped_column(String(255))       # 선수 이름
    team: Mapped[str | None] = mapped_column(String(255))         # 소속 국가대표팀
    team_country: Mapped[str | None] = mapped_column(String(255))  # 소속 국가(전체명)
    position: Mapped[str | None] = mapped_column(String(10))       # GK/DF/MF/FW
    age: Mapped[int | None] = mapped_column(Integer)               # 나이
    birth_year: Mapped[int | None] = mapped_column(Integer)        # 출생 연도
    club: Mapped[str | None] = mapped_column(String(255))          # 소속 클럽
    games: Mapped[int | None] = mapped_column(Integer)             # 출전 경기 수
    minutes: Mapped[float | None] = mapped_column(Numeric)         # 총 출전 시간(분)
    goals: Mapped[float | None] = mapped_column(Numeric)           # 득점
    assists: Mapped[float | None] = mapped_column(Numeric)         # 도움
    cards_yellow: Mapped[float | None] = mapped_column(Numeric)    # 경고 수
    cards_red: Mapped[float | None] = mapped_column(Numeric)       # 퇴장 수


# --- Match 모델 (경기 테이블) -------------------------------
class Match(Base):
    __tablename__ = 'matches'

    id: Mapped[int] = mapped_column('matches_id', Integer, primary_key=True)

    round: Mapped[str | None] = mapped_column(String(50))           # 라운드(조별리그/16강 등)
    date: Mapped[str | None] = mapped_column(Date)                  # 경기 날짜 (KST 기준)
    start_time: Mapped[str | None] = mapped_column(Time)            # 시작 시각 (KST 기준)
    home_team: Mapped[str | None] = mapped_column(String(255))
    away_team: Mapped[str | None] = mapped_column(String(255))
    score: Mapped[str | None] = mapped_column(String(20))           # 예: '2-1'
    home_score: Mapped[float | None] = mapped_column(Numeric)
    away_score: Mapped[float | None] = mapped_column(Numeric)
    venue: Mapped[str | None] = mapped_column(String(255))          # 경기장
    referee: Mapped[str | None] = mapped_column(String(255))
    home_manager: Mapped[str | None] = mapped_column(String(255))
    away_manager: Mapped[str | None] = mapped_column(String(255))
    attendance: Mapped[int | None] = mapped_column(Integer)         # 관중 수


# --- Team 모델 (팀 집계 테이블) -----------------------------
class Team(Base):
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column('teams_id', Integer, primary_key=True)

    team: Mapped[str | None] = mapped_column(String(255))
    team_country: Mapped[str | None] = mapped_column(String(255))
    players_used: Mapped[int | None] = mapped_column(Integer)       # 기용된 선수 수
    avg_age: Mapped[float | None] = mapped_column(Numeric)          # 평균 나이
    possession: Mapped[float | None] = mapped_column(Numeric)       # 평균 점유율(%)
    games: Mapped[int | None] = mapped_column(Integer)
    goals: Mapped[int | None] = mapped_column(Integer)
    assists: Mapped[int | None] = mapped_column(Integer)
    goals_against: Mapped[int | None] = mapped_column(Integer)      # 실점(상대 기준)


# --- PlayerE 모델 (선수 테이블) -----------------------------
class PlayerE(Base):
    __tablename__ = 'playerse'  # 실제 DB 테이블 이름

    # DB 컬럼명은 players_id 인데, 파이썬에서는 짧게 id로 쓰고 싶어서
    # mapped_column('players_id', ...) 처럼 컬럼명을 직접 지정
    id: Mapped[int] = mapped_column('players_id', Integer, primary_key=True)

    player: Mapped[str | None] = mapped_column(String(255))       # 선수 이름
    team: Mapped[str | None] = mapped_column(String(255))         # 소속 국가대표팀
    team_country: Mapped[str | None] = mapped_column(String(255))  # 소속 국가(전체명)
    position: Mapped[str | None] = mapped_column(String(10))       # GK/DF/MF/FW
    age: Mapped[int | None] = mapped_column(Integer)               # 나이
    birth_year: Mapped[int | None] = mapped_column(Integer)        # 출생 연도
    club: Mapped[str | None] = mapped_column(String(255))          # 소속 클럽
    games: Mapped[int | None] = mapped_column(Integer)             # 출전 경기 수
    minutes: Mapped[float | None] = mapped_column(Numeric)         # 총 출전 시간(분)
    goals: Mapped[float | None] = mapped_column(Numeric)           # 득점
    assists: Mapped[float | None] = mapped_column(Numeric)         # 도움
    cards_yellow: Mapped[float | None] = mapped_column(Numeric)    # 경고 수
    cards_red: Mapped[float | None] = mapped_column(Numeric)       # 퇴장 수
