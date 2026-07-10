# ================================================
# TEST/08_빅데이터저장시스템개발_김동욱/pipeline.py
#
# 전체 파이프라인 통합 실행
#   1. init_db()         - 테이블 생성
#   2. load_water_csv()  - water.csv 적재
#   3. load_area_csv()   - area.csv 적재
#   4. verify()          - 적재 검증
# ================================================
from database import init_db
from loader import load_water_csv, load_area_csv
from verify import verify


def run_pipeline():
    print("\n=== 테이블 준비 ===")
    init_db()

    print("\n=== 데이터 적재 ===")
    load_water_csv()
    load_area_csv()

    print("\n=== 적재 검증 ===")
    return verify()

if __name__ == "__main__":
    run_pipeline()