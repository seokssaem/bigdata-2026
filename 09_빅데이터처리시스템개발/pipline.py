import config 
from database import  check_required_tables
from batch_processor import  run_batch_processing
from event_processor import run_event_processing
from verify_processing import verify

def main():
    print('DB 접속정보 환경변수 설정')

    print('engine 생성 및 공통 유틸리티')
    check_required_tables()

    print('배치 처리 모듈')
    run_batch_processing()
    
    print('이벤트 처리 모듈')
    run_event_processing()

    print('[System] 모든 데이터 처리 파이프라인이 성공적으로 완료되었습니다.')

    print('처리 결과 검증')
    verify()

if __name__ == '__main__':
    main()