# 빅데이터 수집 시스템 개발 테스트

## 사용 API
- 공공데이터포털 → 국토교통부_(TAGO)_버스노선정보 → 노선번호목록 조회
- http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getRouteNoList

## 데이터 처리
- 도시코드 목록 조회(http://apis.data.go.kr/1613000/BusRouteInfoInqireService/getCtyCodeList)
    - 대구 도시코드 : 22 확인
- ['response']['body']['items']['item'] → 데이터프레임 생성
- 컬럼 이름 한글로 변환
- 노선ID, 노선번호, 기점, 종점 컬럼 추출
- datetime 라이브러리의 today() 함수 이용 → 수집일시 컬럼 추가

## DB 저장
- PostgreSQL에 DB 저장
- DB 이름 : bigdatatestdb
- table 이름 : bus

## CSV 저장
- 저장 경로
    - c:\Users\Administrator\bigdata2026\fastapi\bus_pipeline\output\bus.csv