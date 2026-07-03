# 공항 혼잡도 API 데이터 수집
## 프로젝트 개요
공공데이터포털 OpenAPI를 이용하여 공항 혼잡도 데이터를 수집하고, 전처리한 후 PostgreSQL 데이터베이스에 저장하는 프로그램
## 수행 내용
- requests를 이용하여 공항 혼잡도 OpenAPI 데이터 수집
- JSON 데이터를 pandas DataFrame으로 변환
- 수집일시와 혼잡여부 파생 컬럼 추가
- 데이터 행 개수와 결측치 확인을 통한 유효성 검증
- SQLAlchemy의 to_sql()을 이용하여 PostgreSQL에 데이터 저장