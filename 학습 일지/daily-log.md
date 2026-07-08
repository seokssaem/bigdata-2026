# 학습일지 (daily-log.md)

## 작성자
* 이름 : 태두혁

---

## 2026-06-15
- FATSAPI 블로그 포스트 검색, 생성, 수정 및 삭제 기능 복습
- HTMI/CSS 수업 내용 복습
    https://github.com/TaeGaori/fastapi_2026/tree/main/blog


## 2026-06-16
- FASTAPI 오늘 뭐먹지?? 복습
    https://github.com/TaeGaori/fastapi_2026/blob/main/%EC%8B%A4%EC%8A%B5/07_%EC%A0%90%EC%8B%AC%EB%A9%94%EB%89%B4.py

## 2026-06-17
- 토이 프로젝트 게임 캐릭터 만들기
    https://github.com/TaeGaori/bigdata-basic/blob/main/Practice/Toy_Project.py
    

## 2026-06-18
- fastapi -> routers(회원가입) 복습
    https://github.com/TaeGaori/fastapi_2026/tree/main/routers

## 2026-06-17
- html + css를 활용하여 대시보드 웹페이지 만들기 복습

## 2026-06-22
- html 애니매이션을 활용하기 
    - translate     (현재 위치에서 x,y축으로 이동)
    - scale         (확대 or 축소)
    - rotate        (중심축 기준으로 회전)
    - perpective    (3D변형할 때입체감)
    - skew          (비틀거나 기울임)
    - product       ()
    - animation     (시간에 따라 변화시킴)

## 2026-06-23
- html총 정리 (원두 사이트)
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/stylc.css

## 2026-06-24
- SQLE 기초 공부
    SELECT   컬럼명           -- 1. 뭘 볼지
    FROM     테이블명          -- 2. 어디서
    WHERE    조건             -- 3. 어떤 조건으로
    GROUP BY 그룹기준          -- 4. 어떻게 묶을지
    HAVING   그룹조건          -- 5. 묶은 결과 조건
    ORDER BY 정렬기준          -- 6. 어떻게 정렬할지
    LIMIT    숫자             -- 7. 몇 개만 볼지

    안 쓰는 건 가능하지만 사용한다면 순서 지키기!


- html 원두 사이트를 활용하여 나만의 페이지로 편집
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/stylc.css


## 2026-06-25
- SQLD JOIN을 사용하여 두 테이블 연결하기

## 2026-06-26
- SQLD  시험에 나올 기출문제 실습 및 연습문제 풀기

## 2026-06-29
- fastapi 복습
    - CRUD --> 데이터를 다루는 4가지 기본 동작
        -Create : 생성 POST(Fastapi) INSERT(SQL)     --> ex.회원가입, 글 작성
        -Read   : 조회 GET(FastAPI) SELECT(SQL)      --> ex.목록 보기, 상세 보기
        -Update : 수정 PUT/PATCH(FastAPI) UPDATE(SQL)--> ex.정보 수정
        -Delete : 삭제 DELETE(FastAPI) DELETE(SQL)   --> ex. 회원 탈퇴, 글 삭제

    - sql_databases --> User + Item, 1:N 관계 CRUD
        - 공식 FastAPI 튜토리얼 예제를 PostgreSQL로 변환한 버전
        - 'User'(사용자)가 여러 개의 'Item' (아이템)을 소유하는 **1:N** 구조
        - 'crud.py'를 별도로 분리하여 DB 조작 로직과 라우터 로직을 나눔
    
    - __init__.py 생성 이유:  오류 방지
    https://github.com/TaeGaori/fastapi_2026/tree/main/fastapi_review

## 2026-06-30
- 판다스를 활용하여 엑셀 파일 읽고 병합 + 시각화
    https://github.com/TaeGaori/fastapi_2026/tree/main/fastapi_review

- fastapi로 main 테스트하기.
        pytest 라이브러리 --> python 표준 테스트 도구
        파일과 함수 이름은 test_로 시작
        권장사항 > 테스트 DB도 따로 만들어준다.
        uv add pytest --> 설치  
    https://github.com/TaeGaori/bigdata-basic/blob/main/happy/ch09_happy.ipynb


## 2026-07-01
- 데이터 수집 파이프라인 - csv파일 방식
    - 전체 파이프라인 흐름
        1. 환경설정 : 라이브러리 불러오기, 경로, DB URL 설정
        2. 수집     : csv 파일 읽기 (인코딩 --> 원도 cp949)
        3. 변환     : 파일에 따라
        4. 파생컬럼(파생변수) : ex) 시작시 / 날짜 / 요일코드 / 주말여부
        5. 검증 : 유효성 검증 리포트 출력
        6. DB 저장 : PostgreSQL -> subwaydb
        7. csv 저장 : output폴더 안 csv파일 (utf-8)
    https://github.com/TaeGaori/fastapi_2026/blob/main/01_subway_pipeline/01_subway.ipynb
- 응용 (공용주차장 CSV 컬럼추출)
    https://github.com/TaeGaori/fastapi_2026/blob/main/02_parking/02_parking.ipynb

## 2026-07-02
- 데이터 수집 파이프라인 - API방식
    - 전체 파이프라인 흐름
            1. 공공데이터포털에서 원하는 API 활용 신청
            2. API 키 준비(.env), 기본 설정 준비(dotenv)
            3. 수집 : JSON 구조 확인, 전체 페이지 수집
            4. 판다스의 데이터프레임 만들기
            5. 변환 : 데이터 확인, 컬럼명, 자료형
            6. 파생컬럼(파생변수) 추가
            7. 데이터 검증( 생략 가능)
            8. DB 저장 : 먼저 pgAdmin에서 데이터베이스 생성(busapidb) -> 테이블 저장
            9. CSV 저장 : bus_stop.csv 인코딩 설정 (utf-8)
    https://github.com/TaeGaori/fastapi_2026/blob/main/03_bus_api_pipeline/03_bus_api.ipynb

- 응용 (정류소별 경유노선 API 조회)
    https://github.com/TaeGaori/fastapi_2026/blob/main/03_bus_api_pipeline/03_node.ipynb

## 2026-07-03
- 데이터 수집 TEST - AP방식
    - 검색 지역의 1등 당첨 상호명과 횟수 수집 후 DB에 저장


## 2026-07-06
- SQLAlchemy 에서 대체키+UNIQUE 선언
    __table_arge__ = (
    UniqueConstraint("컬럼1","컬럼2","컬럼3",... name="제약조건이름")
)

`__table_args__`:
- 테이블 레이블의 부가설정(제약조건, 인덱스 등)을 담는 클래스 속성
- SQLAlchemy가 이름 보고 자동 인식
- 콤마룰 붙여 튜플로 인식시켜야 함

`UniqueConstraint("컬럼1","컬럼2","컬럼3",... name="제약조건이름")`
- 나열된 컬럼들의 조합이 테이블 전체에서 유일
- name= 필수 x 에러나 제약조건 참조할 때 필요한 경우 많아 관례상 붙임

- 전체 파이프 라인
    1. 테이블 재설계
    2. 기존 테이블 삭제 재설계한 모델로 다시 생성
    3. CSV -> DB 배치 적재

## 2026-07-07
- SQLAlchemy 에서 자연키+merge 선언

## 2026-07-08
- SQLAlchemy 모델 정의
    관계 정의 구분법
    - 1:N : 중간다리 필요 X
            ForeignKey만 있다(외래키 있는 클래스가 N)
    
    - N:M : 중간 테이블 필요
            secondary가 있다 (1:N 생각할 필요 X)