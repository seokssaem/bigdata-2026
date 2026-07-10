from database import init_db
from loader import load_from_csv
from verify import verify

def main():
    print('1) 저장 구조 준비')
    init_db()

    print()
    print('2) apt_deal.csv 적재')
    load_from_csv()

    print()
    print('3) 적재 검증')
    verify()

if __name__ == '__main__':
    main()