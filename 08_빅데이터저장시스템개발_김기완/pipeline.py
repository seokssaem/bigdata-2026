from database import init_db
from loader import load_from_csv
from verify import verify

def main():
    print('1) 저장 구조 준비 (복합 기본키 반영)')
    init_db()

    print()
    print('2) airport_congestion.csv 적재 (merge upsert)')
    load_from_csv()

    print()
    print('3) 적재 검증 실행')
    verify()

if __name__ == '__main__':
    main()