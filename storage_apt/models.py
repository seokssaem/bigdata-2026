from sqlalchemy import Column, Integer, String, Date, Numeric, BigInteger
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class AptDeal(Base):
    __tablename__ = 'apt_deal'

    id = Column(Integer, primary_key=True, autoincrement=True)
    단지명 = Column(String(100), nullable=False)
    법정동 = Column(String(20), nullable=False)
    계약날짜 = Column(Date, nullable=False)
    거래금액 = Column(BigInteger, nullable=False)
    평당가격 = Column(Numeric(20,1), nullable=True)
    전용면적 = Column(Numeric(10,2), nullable=False)
    층 = Column(Integer, nullable=True)
    층구간 = Column(String(10), nullable=True)
    건축년도 = Column(Integer, nullable=False)
    건물연령 = Column(Integer, nullable=True)

    # 같은 단지, 같은 면적, 같은 가격, 같은 날짜에 거래를 한 사람이
    # 여러 명일 수도 있으므로
    # 복합 UNIQUE 제약 조건은 걸지 않는다

    def __repr__(self):
        return f'<AptDeal {self.단지명} {self.계약날짜} {self.거래금액}>'