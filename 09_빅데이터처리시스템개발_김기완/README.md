# 공항 혼잡도 처리시스템 구현

## 프로젝트 개요
저장시스템 단계에서 구축된 PostgreSQL의 원본 데이터를 가공 및 분석하여 범주형 집계 배치 테이블을 생성하고, 특정 임계치 데이터를 추출하는 이벤트 경보 시스템 및 자동 검증 파이프라인 프로그램

## 주요 기능 및 모듈 설명
- **config.py**: 데이터베이스 연동 및 이벤트 임계값 환경변수 관리
- **database.py**: 데이터베이스 연결 엔진 및 다중 스크립트 트랜잭션 처리 공통 유틸리티 구현
- **batch_processor.py**: 범주형 변수(`혼잡여부`) 기준 그룹 집계 결과 테이블(`traffic_airport_batch_summary`) 생성 및 인덱싱 최적화
- **event_processor.py**: 숫자형 변수(`전체_혼잡도`) 임계값 이상인 이상 징후 이벤트를 안전하게 바인딩하여 결과 테이블(`traffic_airport_event_alerts`)에 저장
- **verify_processing.py**: 테이블 생성 상태 및 데이터 카운트 자동 검증 프로세스 구현
- **pipeline.py**: 전체 처리 시스템 모듈을 하나로 결합하여 일괄 자동 실행 제어

## 1. 전제 조건 및 입력 테이블
- **사용 데이터베이스**: `airportdb`
- **입력 테이블**: `airport_congestion`
- **테스트 데이터 특징**: 현재 샘플 데이터의 전체 혼잡도가 1.0~2.0 사이에 분포함에 따라, 시스템 필터링 동작을 명확히 증명하기 위해 이벤트 임계값(Threshold)을 `2.0`으로 설정

## 2. 결과 테이블 목록
- `traffic_airport_batch_summary` (범주형 컬럼 기준 배치 집계 테이블)
- `traffic_airport_event_alerts` (숫자형 컬럼 기준 이벤트 알림 테이블)

## 3. 실행 방법
프로젝트 폴더로 이동한 후, 통합 파이프라인 스크립트를 실행합니다.
cd 09_processing_system
python pipeline.py