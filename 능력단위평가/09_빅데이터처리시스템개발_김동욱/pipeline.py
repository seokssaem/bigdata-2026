# ================================================
# 09_빅데이터처리시스템개발_김동욱/pipeline.py
#     - 전체 통합 실행
# ================================================
from batch_processor import run_batch_processing
from event_processor import run_event_processing
from verify_processing import verify


def run_pipeline():
    """
    배치 처리 : 정수장 및 구분별 분기별 탁도, ph, 잔류염소 평균 정리
    이벤트 처리 : 전체 데이터에서 잔류염소 0.74 초과인 데이터만 알림
    반환 : 잘 처리되었는지 검증
    """
    run_batch_processing()
    run_event_processing()
    return verify()

if __name__ == "__main__":
    run_pipeline()
