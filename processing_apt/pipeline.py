from batch_processor import run_batch_processing
from event_processor import parse_args, run_event_processing
from verify_processing import verify

def main():
    print('[batch] 배치 처리 시작')
    run_batch_processing()

    print()
    print('[event] 이벤트 처리 시작')
    args = parse_args()
    run_event_processing(price_multiplier=args.price_multiplier)

    print()
    print('[verity] 처리시스템 검증')
    verify()

if __name__ == '__main__':
    main()