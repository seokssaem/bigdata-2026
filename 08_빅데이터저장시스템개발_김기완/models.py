from sqlalchemy import Column, String, Numeric, Date
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AirportCongestion(Base):
    __tablename__ = 'airport_congestion'

    공항코드 = Column(String(10), primary_key=True)
    수집시간 = Column(String(10), primary_key=True)
    수집일시 = Column(Date, primary_key=True)
    
    A구역_혼잡도 = Column(Numeric(3, 1), nullable=True)
    B구역_혼잡도 = Column(Numeric(3, 1), nullable=True)
    C구역_혼잡도 = Column(Numeric(3, 1), nullable=True)
    전체_혼잡도 = Column(Numeric(3, 1), nullable=True)
    혼잡여부 = Column(String(20), nullable=True)

    def __repr__(self):
        return f'<AirportCongestion {self.공항코드} {self.수집일시} {self.수집시간} ({self.혼잡여부})>'