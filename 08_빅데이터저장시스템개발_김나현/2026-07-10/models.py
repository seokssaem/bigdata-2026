# =======================================
# 기술은행 수요기술 조회 서비스/models.py
# =======================================
from sqlalchemy import Column, Integer, String, Date, UniqueConstraint
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Tech(Base):
    """
    기술 정보를 담는 테이블
    기술은행에 등록된 기술 = 1행
    """
    __tablename__ = 'tech'

    희망구매유형 = Column(String, nullable=False)
    수요기술명 = Column(String, nullable=False)
    수요기술번호 = Column(Integer, primary_key=True, autoincrement=True)
    진행상태 = Column(String, nullable=False)
    구매희망시기 = Column(String, nullable=False)
    희망기술개요 = Column(String, nullable=False)
    키워드 = Column(String, nullable=False)
    기술도입지원기관 = Column(String, nullable=False)
    기술지표상세 = Column(String, nullable=False)
    기술구매조건 = Column(String, nullable=False)
    기술이전계약설명 = Column(String, nullable=False)
    기술이전계약유형 = Column(String, nullable=False)
    정액기술료 = Column(String, nullable=False)
    기타계약조건 = Column(String, nullable=False)
    경상기술료 = Column(String, nullable=False)
    기술센터지역 = Column(String, nullable=False)
    수집일시 = Column(Date, nullable=False)
    정보충실도 = Column(Integer, nullable=False)
    
    # 복합 UNIQUE 제약 조건 --> "수요기술명 + 진행상태 + 기술도입지원기관" --> 1개만 있어야 한다.
    __table_args__ = (
        UniqueConstraint(
            '수요기술명','진행상태','기술도입지원기관', name='uq_tech_key'
        ),
    )

    def __repr__(self):
        return f'<Tech {self.수요기술명} {self.진행상태} {self.기술도입지원기관}>' 
