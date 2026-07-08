# 빅데이터 저장시스템 개발 - NCS
- 빅데이터 저장모델 설계
- 빅데이터 적재모듈 개발

## 카페 주문 데이터 저장 시스템 실습
## orders 테이블 --> 대체키 + UNIQUE

|파일명|설명|
|---|---|
|`medels.py` | SQRALchemy 테이블 모델 정의(menu: 자연키 / order:  대체키 + UNIQUE)|
|`detabase.py` | DB 연결과 테이블 생성|
|`loader.py`|CSV 적재(menu: merge / orders: 배치 insert)|
|`verify.py`|검증. 대상 테이블 정확히 조사|
|`pipeline.py`|통합 실행|
|`README.me`| 실행 방법과 설계 설명|
|`input/orders.csv`|주문내역 (대체키+UNIQUE 실습용, 중복 행 포함)|

---
### pgAdmin에서 데이터베이스 준비
```sql
CREATE DATABASE cafedb;
```

### 입력 파일 준비

|폴더|필요한 파일|
|---|---|
|`C:\Users\Administrator\bigdata2026\fastapi\storage_cafe_order_api\input`|`order.csv`|