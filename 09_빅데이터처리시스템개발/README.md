# 로또 데이터 처리 및 이상치 탐지 파이프라인 시스템

본 프로젝트는 PostgreSQL 데이터베이스와 SQLAlchemy를 활용하여 대용량 로또 당첨 데이터의 유효성을 검증하고, 지역별 통계 요약(Batch) 및 데이터 이상치 탐지(Event)를 자동화하는 통합 데이터 가공 파이프라인 시스템입니다.

## 전체 시스템 아키텍처 및 흐름
1. **배치 통계 가공 (Batch Processing)**: 주소지 앞 두 글자(시/도 단위) 기준 자동 당첨 건수 총합 요약
2. **이벤트 모니터링 (Event Processing)**: 지정된 당첨 횟수 범위를 만족하거나 지정 구역(대구)의 데이터 추출

---

## 프로젝트 파일 구조

* `main.py`: 전체 데이터 처리 파이프라인의 오케스트레이션을 담당하는 마스터 통합 실행 파일
* `config.py`: 데이터베이스 접속 주소(URL), 탐지 범위, 지역 필터 등 핵심 상수 및 환경변수 설정 파일
* `database.py`: SQLAlchemy 엔진 생성 및 다중 SQL 연속 실행, 필수 테이블 존재 여부 검증 등 공통 유틸리티 모듈
* `batch_processor.py`: 원본 데이터를 압축 및 그룹화하여 통계 요약 테이블을 생성하는 배치 가공 모듈
* `event_processor.py`: 이상치 탐지 알림 테이블을 초기화하고 조건별 장애 징후 데이터를 필터링하는 모니터링 모듈
* `verify_processing.py`: 배치 가공하여 생성된 테이블을 검증하는 모듈

---

## 데이터베이스 테이블

### 1. 지역별 통계 요약 테이블
* **테이블명**: `address_lottery_win_summary`
* **설명**: `lottery_win` 원본에서 지역 앞 두 글자를 그룹화(`GROUP BY`)하여 통계를 낸 결과

### 2. 이상치 탐지 알림 테이블
* **테이블명**: `address_lottery_event_alerts`
* **구조**:
  - `id` (BIGSERIAL, PK): 고유 ID (자동 증가)
  - `event_type` (VARCHAR): 이벤트 유형 (`WIN_COUNT_IN_OF_RANGE` / `LOTTERY_LOCATION_GROUP`)
  - `store_name` (VARCHAR): 상호
  - `store_reigon` (VARCHAR): 지역
  - `metric_value` (INTEGER): 자동당첨건수
  - `detail` (TEXT): 탐지 사유 및 가공 상세 메시지
  - `detected_at` (TIMESTAMP): 파이프라인이 정상 가동되어 이상치가 탐지된 실시간 컴퓨터 타임스탬프

---

## 실행 및 운영 방법

### 1. 데이터베이스 연결 정보 설정
`config.py` 파일 내에 연결할 PostgreSQL 주소를 정확히 기재합니다.
```python
LOTTERAPI_DB_URL = "postgresql://postgres:1234@localhost:5432/lotteryapidb"
```

### 2. 통합 파이프라인 구동
터미널에서 마스터 제어 파일인 `main.py`를 실행하면 세 부문(검증 -> 배치  이벤트)이 연쇄적으로 자동 처리됩니다.
```bash
python main.py
```

### 3. ==== 처리시스템 결과 검증 
터미널에서 검증 파일인 `verify_processing.py`를 실행하여 앞서 처리했던 결과를 재검증할 수 있다.

### 3. 정상 실행 로그 예시
```text
DB 접속정보 환경변수 설정
engine 생성 및 공통 유틸리티
배치 처리 모듈
이벤트 처리 모듈
[event] 당첨 횟수/지역 이벤트 탐지 완료
[System] 모든 데이터 처리 파이프라인이 성공적으로 완료되었습니다.
==== 처리시스템 결과 검증 (배치 + 이벤트) ====
address_lottery_event_alerts: 48건
address_lottery_win_summary: 16건
검증 결과: PASS
```