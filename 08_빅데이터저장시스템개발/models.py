from sqlalchemy import Column, String, Integer, Numeric, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class lottery(Base):
    __tablename__ = 'lottery_win'

    순번 = Column(Integer, nullable=False)
    상호 = Column(String(300), primary_key=True)
    지역 = Column(String(500), nullable=False)
    자동당첨건수 = Column(Integer, nullable=True)

    def __repr__(self):
        return f'<lottery {self.순번} {self.자동당첨건수} {self.상호} {self.지역}>'