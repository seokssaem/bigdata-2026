# ======================================================
# 기술은행 수요기술 조회 서비스/pipeline.py
# ======================================================

from batch_processor import run_batch_processing
from event_processor import parse_args, run_event_processing
from verify_processing import verify
# <<검증 모듈>>

def main():
    args = parse_args()

    print('1) 집계 테이블 생성 및 배치 적재')
    run_batch_processing() 

    print()
    print('2) 이벤트 처리')
    run_event_processing(tech_threshold=args.tech_threshold)

    print()
    print('3) 적재 검증')
    verify() # 검증 함수 호출

if __name__ == '__main__':
    main()