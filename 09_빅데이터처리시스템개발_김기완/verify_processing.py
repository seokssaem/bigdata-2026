from database import airport_engine, table_count

def verify_results() -> bool:
    print('[verify] 처리 결과 검증 자동화 시작')
    try:
        batch_count = table_count(airport_engine, "traffic_airport_batch_summary")
        event_count = table_count(airport_engine, "traffic_airport_event_alerts")
        
        print(f' -> 배치 집계 테이블 건수: {batch_count}건')
        print(f' -> 이벤트 알림 테이블 건수: {event_count}건')
        
        is_success = batch_count > 0
        print(f'[verify] 검증 자동화 결과: {"통과" if is_success else "실패"}')
        return is_success
    except Exception as exc:
        print(f'[verify] 검증 에러 발생: {exc}')
        return False

if __name__ == '__main__':
    verify_results()