# 빅데이터 처리 시스템 실습

## 입력 테이블
- 사용 데이터 : 서울 강남구 아파트 매매 실거래가(2026년 6월)
- `aptapidb` > `apt_deal`

## 결과 테이블
| DB | table |
| --- | --- |
| `aptapidb` | `apt_dong_summary` |
| `aptapidb` | `apt_price_event_alerts` |

## 실행 순서
```bash
# 실행 코드
python pipeline.py
```

1. 배치 처리 : `run_batch_processing()`
    - 필수 테이블 확인 : `check_required_table()`
    - 법정동별 집계 : `create_apt_dong_summary()`

2. 이벤트 처리 : `run_event_processing()`
    - 필수 테이블 확인
        - `check_required_table()`
        - `check_dong_summary_ready()`
    - 이벤트 처리 테이블 준비 : `init_price_alert_table()`
    - 가격 이상치 이벤트 탐지 : `detect_price_outliers()`

3. 검증 : `verify()`