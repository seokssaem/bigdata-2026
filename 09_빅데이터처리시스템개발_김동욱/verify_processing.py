# =================================================================================================
# 09_빅데이터처리시스템개발_김동욱/verify_processing.py
#     - 처리 결과 검증
# =================================================================================================
from database import water_engine, table_count

# CHECKS - 무엇을 검증할지 데이터로 모아둔 리스트
CHECKS = [
    (water_engine, "batch_water_summary"), # 배치 처리 결과 : 정수장 및 구분별 분기별 탁도, ph, 잔류염소 평균 정리
    (water_engine, "event_water_chlorine_alert"), # 이벤트 처리 결과 : 전체 데이터에서 잔류염소 0.74 초과인 데이터만 알림
]

def verify() -> bool:
    """
    CHECKS에 정의된 모든 테이블을 순회하며 건수를 출력하고, 하나라도 조회에 실패하면 전체 결과를 FAIL로 판정

    반환값:
        True: 모든 테이블 조회에 성공 (PASS)
        False: 하나 이상의 테이블 조회에 실패 (FAIL)
    """
    print("==== 처리시스템 결과 검증 (배치 + 이벤트) ====")

    ok = True

    for engine, table_name in CHECKS:
        try:
            count = table_count(engine, table_name)
            print(f"{table_name} : {count:,}건")
        
        except Exception as exc:
            ok = False
            print(f"{table_name} : 확인 실패 - {exc}")

    print(f"검증 결과 : {'PASS' if ok else 'FAIL'}")

    return ok

if __name__ == "__main__":
    verify()