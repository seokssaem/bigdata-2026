
from sqlalchemy import text
from database import ntb_engine, table_count

# CHECKS - 무엇을 검증할 지 데이터로 모아둔 리스트
CHECKS = [
    (ntb_engine, "tech_region_summary"), # 지역별 정보충실도 집계
    (ntb_engine, "tech_status_summary"), # 진행상태별 집계
    (ntb_engine, "missing_fee_event_alerts"), # 기술료 미기재 확인 이벤트
    (ntb_engine, "low_information_event_alerts") # 정보충실도 미달 확인 이벤트
]

def verify() -> bool:
    """
    CHECKS에 정의된 모든 테이블을 순회하며 건수를 출력하고, 하나라도 조회에 실패하면
    전체 결과를 FAIL로 판정
    
    반환값: 
        True: 모든 테이블 조회에 성공 (PASS)
        False: 하나 이상의 테이블 조회에 실패 (FAIL)
    
    """
    print('===== 처리 시스템 결과 검증 (배치+이벤트) =====')

    # 처음에는 성공으로 가정하고, 실패를 한번이라도 만나면 false
    ok = True

    for engine, table_name in CHECKS:
        try:
            count = table_count(engine, table_name) # 함수 호출
            print(f'{table_name}: {count:,}건')
        except Exception as exc:
            ok = False
            print(f'{table_name}: 확인 실패 = {exc}')

    print(f'검증 결과: {"PASS" if ok else "FAIL"}')

    # 호출한 코드가 화면 문자열을 다시 분석하지 않고도 성공여부를 사용할 수 있게 bool값 반환
    return ok

if __name__ == '__main__':
    verify() # 검증 함수 호출