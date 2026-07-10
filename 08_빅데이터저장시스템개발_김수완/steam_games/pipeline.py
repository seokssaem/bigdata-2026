# ======================================================
# steam_games/pipeline.py
#
# Steam 게임 데이터 저장 파이프라인 통합 실행
#   1) 저장 구조(재)설계  2) CSV 배치 적재  3) 적재 검증
# ======================================================

from database import init_db
from loader import load_from_csv
from verify import verify


def main():
    print('1) 저장 구조 재설계 (기본키 + UNIQUE/FK 제약 적용)')
    init_db()

    print()
    print('2) games.csv 배치 적재')
    load_from_csv()

    print()
    print('3) 적재 검증')
    verify()


if __name__ == '__main__':
    main()
