# ======================================================
# 기술은행 수요기술 조회 서비스/pipeline.py
# ======================================================

from database import init_db
from loader import load_from_csv
from verify import verify
# <<검증 모듈>>

def main():
    print('1) 저장 구조 재설계 (기본키 + UNIQUE 제약 적용)')
    init_db()  # 함수 호출

    print()
    print('2) 결과(NTB_db.csv) 배치 적재')
    load_from_csv()  # 함수 호출

    print()
    print('3) 적재 검증')
    verify() # 검증 함수 호출

if __name__ == '__main__':
    main()