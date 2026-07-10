# ================================================
# steam_games/models.py
#
# 저장 모델 설계(스키마)
#   games       : 게임 기본정보 (자연키 app_id 보유 -> 기본키로 사용)
#   game_genres      : 게임-장르 (1:N, 콤마 다중값 컬럼 정규화)
#   game_categories  : 게임-카테고리 (1:N)
#   game_tags        : 게임-태그 (1:N)
#   game_developers  : 게임-개발사 (1:N)
#   game_publishers  : 게임-퍼블리셔 (1:N)
#
# 직접 실행되는 파일은 아니다.
#   database.py, loader.py 가 import해서 사용
# ================================================

# 라이브러리 불러오기
from sqlalchemy import (
    Column, Integer, SmallInteger, String, Date, Numeric,
    ForeignKey, UniqueConstraint,
)
from sqlalchemy.orm import declarative_base, relationship

# 모든 모델 클래스가 상속받을 선언적 베이스 클래스를 생성
# 이 Base를 상속받으면 클래스=테이블, 클래스 속성=컬럼으로 자동 매핑
Base = declarative_base()


class Game(Base):
    # 실제 PostgreSQL에 생성될 테이블 이름
    __tablename__ = 'games'

    # 자연키(natural key): Steam이 게임마다 부여하는 고유 식별자
    # AppID 자체가 이미 고유값이므로 대체키(surrogate id) 없이 바로 기본키(PK)로 사용
    app_id = Column(Integer, primary_key=True, autoincrement=False)

    # 실제 데이터 컬럼들
    name = Column(String(500), nullable=False)              # 게임 이름
    release_date = Column(Date, nullable=True)               # 출시일 (파싱 실패시 NULL 허용)
    price = Column(Numeric(10, 2), nullable=False, default=0)  # 정가(USD)
    discount = Column(SmallInteger, nullable=False, default=0)  # 할인율(%) 0~100
    owners_min = Column(Integer, nullable=False, default=0)   # 추정 소유자수 하한
    owners_max = Column(Integer, nullable=False, default=0)   # 추정 소유자수 상한
    peak_ccu = Column(Integer, nullable=False, default=0)     # 동시접속자 최고치
    required_age = Column(SmallInteger, nullable=False, default=0)  # 최소 연령 등급
    metacritic_score = Column(SmallInteger, nullable=False, default=0)  # 메타크리틱 점수(0~100)
    positive = Column(Integer, nullable=False, default=0)     # 긍정 리뷰 수
    negative = Column(Integer, nullable=False, default=0)     # 부정 리뷰 수

    # 1:N 관계 (자식 테이블에서 games.app_id를 참조)
    genres = relationship('GameGenre', back_populates='game', cascade='all, delete-orphan')
    categories = relationship('GameCategory', back_populates='game', cascade='all, delete-orphan')
    tags = relationship('GameTag', back_populates='game', cascade='all, delete-orphan')
    developers = relationship('GameDeveloper', back_populates='game', cascade='all, delete-orphan')
    publishers = relationship('GamePublisher', back_populates='game', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Game {self.app_id} {self.name}>'


class GameGenre(Base):
    """게임-장르 1:N (원본 Genres 컬럼: 콤마로 여러 값이 들어있던 컬럼을 정규화)"""
    __tablename__ = 'game_genres'

    # 대체키(surrogate key): 이 테이블 자체는 자연키가 없어서 일련번호로 PK 지정
    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('games.app_id', ondelete='CASCADE'), nullable=False)
    genre_name = Column(String(100), nullable=False)

    game = relationship('Game', back_populates='genres')

    # 자연키가 없는 테이블 -> "같은 게임 + 같은 장르"가 두 번 이상 쌓이지 않도록 UNIQUE 제약
    __table_args__ = (
        UniqueConstraint('app_id', 'genre_name', name='uq_game_genres_key'),
    )


class GameCategory(Base):
    """게임-카테고리 1:N (원본 Categories 컬럼 정규화)"""
    __tablename__ = 'game_categories'

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('games.app_id', ondelete='CASCADE'), nullable=False)
    category_name = Column(String(100), nullable=False)

    game = relationship('Game', back_populates='categories')

    __table_args__ = (
        UniqueConstraint('app_id', 'category_name', name='uq_game_categories_key'),
    )


class GameTag(Base):
    """게임-태그 1:N (원본 Tags 컬럼 정규화)"""
    __tablename__ = 'game_tags'

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('games.app_id', ondelete='CASCADE'), nullable=False)
    tag_name = Column(String(100), nullable=False)

    game = relationship('Game', back_populates='tags')

    __table_args__ = (
        UniqueConstraint('app_id', 'tag_name', name='uq_game_tags_key'),
    )


class GameDeveloper(Base):
    """게임-개발사 1:N (원본 Developers 컬럼 정규화)"""
    __tablename__ = 'game_developers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('games.app_id', ondelete='CASCADE'), nullable=False)
    developer_name = Column(String(200), nullable=False)

    game = relationship('Game', back_populates='developers')

    __table_args__ = (
        UniqueConstraint('app_id', 'developer_name', name='uq_game_developers_key'),
    )


class GamePublisher(Base):
    """게임-퍼블리셔 1:N (원본 Publishers 컬럼 정규화)"""
    __tablename__ = 'game_publishers'

    id = Column(Integer, primary_key=True, autoincrement=True)
    app_id = Column(Integer, ForeignKey('games.app_id', ondelete='CASCADE'), nullable=False)
    publisher_name = Column(String(200), nullable=False)

    game = relationship('Game', back_populates='publishers')

    __table_args__ = (
        UniqueConstraint('app_id', 'publisher_name', name='uq_game_publishers_key'),
    )
