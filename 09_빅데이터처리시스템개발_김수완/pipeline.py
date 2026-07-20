# ================================================================================
# steam_games/pipeline.py
#   - 배치 처리 -> 이벤트 처리 순서로 전체 파이프라인을 한 번에 실행한다.
# ================================================================================
from batch_processor import run_batch_processing
from event_processor import run_event_processing


def main() -> None:
    run_batch_processing()
    print()
    run_event_processing()
    print()
    print('[pipeline] 처리 파이프라인 완료')
    print('pgAdmin Query Tool에서 SELECT COUNT(*)로 결과 테이블을 확인하거나,')
    print('python verify_processing.py 로 자동 검증할 수 있습니다.')


if __name__ == '__main__':
    main()
