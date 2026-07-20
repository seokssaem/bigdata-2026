import batch_processor
import event_processor
import verify_processing

def run_pipeline() -> None:
    print('=============================================')
    print('  공항 혼잡도 처리시스템 통합 파이프라인 구동  ')
    print('=============================================')
    
    batch_processor.main()
    event_processor.main()
    verify_processing.verify_results()
    
    print('=============================================')
    print('  파이프라인 전체 프로세스 완료  ')
    print('=============================================')

if __name__ == '__main__':
    run_pipeline()