from database import init_db
from loader import load_menu
from verify import verify

def main():
    print('1) 저장 구조 준비 (menu: 자연키)')
    init_db()

    print()
    print('2) menu.csv 적재 (merge upsert)')
    load_menu()

    print()
    print('3) 적재 검증')
    verify()

if __name__ == '__main__':
    main()