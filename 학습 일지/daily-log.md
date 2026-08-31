# 학습일지 (daily-log.md)

## 작성자
* 이름 : 태두혁

---

# 2026-06-15
### FATSAPI 블로그 포스트 검색, 생성, 수정 및 삭제 기능 복습
### HTMI/CSS 수업 내용 복습
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/blog

---

# 2026-06-16
### FASTAPI 오늘 뭐먹지?? 복습
    
    https://github.com/TaeGaori/fastapi_2026/blob/main/%EC%8B%A4%EC%8A%B5/07_%EC%A0%90%EC%8B%AC%EB%A9%94%EB%89%B4.py

---

# 2026-06-17
### 토이 프로젝트 게임 캐릭터 만들기
    
    https://github.com/TaeGaori/bigdata-basic/blob/main/Practice/Toy_Project.py
    
---

# 2026-06-18
### fastapi -> routers(회원가입) 복습
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/routers

---

# 2026-06-17
### html + css를 활용하여 대시보드 웹페이지 만들기 복습

---

# 2026-06-22
### html 애니매이션을 활용하기 
    - translate     (현재 위치에서 x,y축으로 이동)
    - scale         (확대 or 축소)
    - rotate        (중심축 기준으로 회전)
    - perpective    (3D변형할 때입체감)
    - skew          (비틀거나 기울임)
    - product       ()
    - animation     (시간에 따라 변화시킴)

---

# 2026-06-23
### html총 정리 (원두 사이트)
    
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/stylc.css

---

# 2026-06-24
### SQLE 기초 공부
    SELECT   컬럼명           -- 1. 뭘 볼지
    FROM     테이블명          -- 2. 어디서
    WHERE    조건             -- 3. 어떤 조건으로
    GROUP BY 그룹기준          -- 4. 어떻게 묶을지
    HAVING   그룹조건          -- 5. 묶은 결과 조건
    ORDER BY 정렬기준          -- 6. 어떻게 정렬할지
    LIMIT    숫자             -- 7. 몇 개만 볼지

    안 쓰는 건 가능하지만 사용한다면 순서 지키기!


### html 원두 사이트를 활용하여 나만의 페이지로 편집
    
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/stylc.css

---

# 2026-06-25
### SQLD JOIN을 사용하여 두 테이블 연결하기

---

# 2026-06-26
### SQLD  시험에 나올 기출문제 실습 및 연습문제 풀기

---

# 2026-06-29
### fastapi 복습
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

---

# 2026-06-30
### 판다스를 활용하여 엑셀 파일 읽고 병합 + 시각화
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/fastapi_review

### fastapi로 main 테스트하기.
        pytest 라이브러리 --> python 표준 테스트 도구
        파일과 함수 이름은 test_로 시작
        권장사항 > 테스트 DB도 따로 만들어준다.
        uv add pytest --> 설치  
    
    https://github.com/TaeGaori/bigdata-basic/blob/main/happy/ch09_happy.ipynb

---

# 2026-07-01
### 데이터 수집 파이프라인 - csv파일 방식
    - 전체 파이프라인 흐름
        1. 환경설정 : 라이브러리 불러오기, 경로, DB URL 설정
        2. 수집     : csv 파일 읽기 (인코딩 --> 원도 cp949)
        3. 변환     : 파일에 따라
        4. 파생컬럼(파생변수) : ex) 시작시 / 날짜 / 요일코드 / 주말여부
        5. 검증 : 유효성 검증 리포트 출력
        6. DB 저장 : PostgreSQL -> subwaydb
        7. csv 저장 : output폴더 안 csv파일 (utf-8)
    
    https://github.com/TaeGaori/fastapi_2026/blob/main/01_subway_pipeline/01_subway.ipynb
### 응용 (공용주차장 CSV 컬럼추출)
    
    https://github.com/TaeGaori/fastapi_2026/blob/main/02_parking/02_parking.ipynb

---

# 2026-07-02
### 데이터 수집 파이프라인 - API방식
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

### 응용 (정류소별 경유노선 API 조회)
    
    https://github.com/TaeGaori/fastapi_2026/blob/main/03_bus_api_pipeline/03_node.ipynb
 
---

# 2026-07-03
### 데이터 수집 TEST - AP방식
    - 검색 지역의 1등 당첨 상호명과 횟수 수집 후 DB에 저장
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/07_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%88%98%EC%A7%91%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%B0%9C

---

# 2026-07-06
### SQLAlchemy 에서 대체키+UNIQUE 선언
    __table_arge__ = (
    UniqueConstraint("컬럼1","컬럼2","컬럼3",... name="제약조건이름")

    `__table_args__`:
    - 테이블 레이블의 부가설정(제약조건, 인덱스 등)을 담는 클래스 속성
    - SQLAlchemy가 이름 보고 자동 인식
    - 콤마룰 붙여 튜플로 인식시켜야 함

    `UniqueConstraint("컬럼1","컬럼2","컬럼3",... name="제약조건이름")`
    - 나열된 컬럼들의 조합이 테이블 전체에서 유일
    - name= 필수 x 에러나 제약조건 참조할 때 필요한 경우 많아 관례상 붙임
### 전체 파이프 라인
    1. 테이블 재설계
    2. 기존 테이블 삭제 재설계한 모델로 다시 생성
    3. CSV -> DB 배치 적재
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/storage_subway_busapi/01_subway

---

# 2026-07-07
### SQLAlchemy 에서 자연키+merge 선언
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/storage_subway_busapi/02_bus

---

# 2026-07-08
### foodball SQLAlchemy 모델 정의
    관계 정의 구분법
    - 1:N : 중간다리 필요 X
            ForeignKey만 있다(외래키 있는 클래스가 N)
    
    - N:M : 중간 테이블 필요
            secondary가 있다 (1:N 생각할 필요 X)
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/cafe

---

# 2026-07-09
### foodball SQLAlchemy test코딩

### seed_postgres_basic.py
    - test_crud.py는 csv파일 직접 읽지 X
    - 따라서 테스트 전 CSV데이터를 PostgreSQL 테이블에 넣고 실행
    - **실행시 기존 테이블이 삭제되고 다시 만들어지기 대문에 중요한 데이터가 있다면 실행 X **
   
   https://github.com/TaeGaori/fastapi_2026/tree/main/football

---

# 2026-07-10
### 데이터 저장 test
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/08_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%A0%80%EC%9E%A5%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%B0%9C

---

# 2026-07-13
### 만들어 둔 DB를 이용하여 데이터 처리 시스템 개발
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/NCS-bigdata_processing.system

---

# 2026-07-14
### NCS 빅데이터 처리 시스템 개발 복습
    - 원본 데이터 탐색
    - 역별 인원 값 집계하기
    - 시간대별 승차 인원 집계하기
    - 날짜별 승·하차 집계하기
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/NCS-bigdata_processing.system

---

# 2026-07-15
### SQLAlchemy 2.0 버전으로 코드 변경

---

# 2026-07-16
### QLAlchemy 2.0 버전으로 코드 마무리
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/football

###   Streamlit 라이브러리 기초 실습
    - 파이썬 코드만으로 웹페이지(대시보드, 데이터시각화 등)을 쉽게 만들 수 있도록 도와주는 파이썬 라이브러리
    - 위젯 단위(버튼 클릭, 슬라이더 이동, 제목 등)

---

# 2026-07-20
###  빅데이터 처리 시스템 개발 test
    
    https://github.com/TaeGaori/fastapi_2026/tree/main/09_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%B2%98%EB%A6%AC%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%B0%9C

---

# 2026-07-21
### 분석데이터전처리

### Streamlit & 실습
    - multiselect : 여러 개의 선택지를 동시에 선택할 수 있는 입력 위젯:
        - `st.multiselect()`는 여러 개의 선택지를 동시에 선택할 수 있는 입력 위젯.
        - `correct`처럼 정답을 `set`으로 저장하면, 순서에 상관없이 값 포함 여부만 비교할 수 있다.
        - `set(fruits) == correct`로 사용자가 고른 값과 정답을 비교.

    - slider : 슬라이더로 값을 선택할 수 있는 위젯(최대 최소 설정 가능)
        - `min_value=time(0`)`	선택 가능한 가장 이른 시간은 00:00
        - `max_value=time(23)`	선택 가능한 가장 늦은 시간은 23:00

    - input :   - `placeholder`: 입력창 안내 문구
                - `max_chars`: 최대 입력 글자 수 제한
                - `type='password'`: 입력값을 로 가림

    - File uploader:- `type='csv'`: 확장자 제한
                    - `accept_multiple_files=False`: 한 번에 하나의 파일만 업로드 가능
                    - `pd.read_csv(file)`로 바로 읽을 수 있습니다.

    https://github.com/TaeGaori/fastapi_2026/tree/main/Steamlit

---

# 2026-07-22
### API 문서화 (메타 데이터 추가) : 처음 보는 다른 개발자가 docs만 보고도 어떻게 사용하는지 이해할 수 있도록 추가 설명을 채운다
    - FastAPI(...) 생성자에 title / version / description 추가
    --> Swagger UI 맨 뒤 소개 영역에 표시된다.
    - 각 @app.get(...)에 summary/ description/ response_description 추가
    --> Swagger UI에서 각 엔드포인트를 펼쳤을 때 보이는 설명이다.
    - 함수 매개변수의 기본값을 Query(...)로 감싸서 파라미터별 설명 추가
    --> Swagger UI의 "Try it out" 화면에서 각 입력 칸 옆에 뜬다.
    - operation_id / tags 추가
    --> operation_id : 이 API를 가리키는 고유한 이름, tags : Swgger UI에서 엔드포인트들을 그룹으로 묶여 보여주는 기준이다.

    https://github.com/TaeGaori/fastapi_2026/blob/main/football/main.py
    
### 데이터 타입 변환 & 결측치 처리 기초
    - apply(pd.to_numeric)  
        -선택한 여러 열에 한 번에 숫자 변환 함수를 적용한다.
    
    - Dropna()
        - 결측값이 있는 행 제거
        - 가장 간단하지만 데이터가 많이 삭제될 수 있어 신중하게 사용해야 한다.
        - 결측치 비율이 매우 낮을 때만 권장한다.
        - 기본값은 행 기준(axis=0)
        - axis=1 --> 열(컬럼) 기준
    
    - fillna()
        - 결측치를 다른 값으로 채운다.

    - mode()
        - 해당 열에서 가장 자주 나온 값들을 리스트 형태로 변환
        - 최반값이 여러개여도 첫번쨰값 불러오기 --> [0]

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/ch10_no_show.ipynb

---

# 2026-07-23
### 데이터 타입 변환 & 결측치 처리 csv파일로 실습

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/ch10_no-show-result(day53).ipynb

### FASTAPI pytest로 단위 테스트
    - test_crud.py : crud.py 함수 호출 -> DB 조회 로직만 검증

        https://github.com/TaeGaori/fastapi_2026/blob/main/football/test_crud.py

    - test_main.py : HTTP요청 흉내 -> URL / 상태코드 / 응답구조 검증 -> API 완성 결정

        https://github.com/TaeGaori/fastapi_2026/blob/main/football/test_main.py

    - TestClient : uvicorn 서버 띄우지 않고 앱 호출하기 때문에 빠르게 같은 결과 확인 가능
    
---

# 2026-07-24
### 조별 토이프로젝트 토의

### 인코딩
    - 통계와 모델을 만들기 위해선 Text(인간 언어) -> Number(숫자)로 통역해 주어야 한다
        - fit : 범주(문자열) 학습
        - transform : 숫자 변환
        - 학습하고 숫자변환을 한 번에 수행

    - pd.get_dummies() : 판다스에서 원핫 인코딩
    - .inverse_transform() : 레이블 인코딩 역변환(디코딩)
    - LabelEncoder : 사이킷런으로 레이블 인코딩

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day54_%EC%9D%B8%EC%BD%94%EB%94%A9.ipynb

### 스케일링
    - 컬럼 간 숫자의 상대적 크기 차이 때문에 생기는 문제들을 해결하기 위한 과정 
    - 정규화, 표준화 이 두가지를 가장 많이 활용
    - 사이킷런 라이브러리에 구현

    - MinMaxScaler = (df_num - df_num.min()) / (df_num.max() - df_num.min())

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day54_%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.ipynb

---

# 2026-07-27
### 왜도 .skew()
    - 데이터 분포가 좌우 대칭에서 얼마나, 어느 방향으로 치우쳐 있는지를 나타내는 지표
    - 왜도가 0 --> 좌우 대칭(정규분포처럼)
    - 왜도 > 0 --> 양의 왜도, 오른쪽으로 긴 꼬리 (대부분의 값은 작은 쪽에 몰려있다. 소수의 큰 값이 꼬리를 늘린다.)
    - 왜도 < 0 --> 음의 왜도, 왼쪽으로 긴 꼬리 (대부분의 값은 큰 쪽에 몰려있다. 소수의 작은 값이 꼬리를 늘린다.)

### 파생 변수 생성 및 스케일링
    - scale_cols = [] -> scaler = StandardScaler() -> df[scale_cols] = scaler.fit_transform(df[scale_cols])

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day54_%EC%8A%A4%EC%BC%80%EC%9D%BC%EB%A7%81.ipynb

### 공유자전거 대여 운영 데이터 전처리와 EDA 실습

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/A_%EA%B3%B5%EC%9C%A0%EC%9E%90%EC%A0%84%EA%B1%B0_%EB%B6%84%EC%84%9D_%ED%83%9C%EB%91%90%ED%98%81.ipynb


# 2026-07-28
### 분석 데이터 전처리 test

    https://github.com/TaeGaori/DATA_ANAYSIS/tree/main/10_%EB%B6%84%EC%84%9D%EB%8D%B0%EC%9D%B4%ED%84%B0%EC%A0%84%EC%B2%98%EB%A6%AC_%ED%83%9C%EB%91%90%ED%98%81

### 탐색적 데이터 분석 test

    https://github.com/TaeGaori/DATA_ANAYSIS/tree/main/11_%ED%83%90%EC%83%89%EC%A0%81%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D_%ED%83%9C%EB%91%90%ED%98%81

---

# 2026-07-29
### 빅데이터 분석 모델링
    - 입력(피처)과 정답(타겟)을 분리 -> 훈련 데이터와 검증 데이터 나누기(사이킷런, train_test_split)

    - 선형 회기(LinearRegression)
        - 연속적인 숫자를 예측하는 모델
        - 최적의 직선을 찾는 방법론
        - 기울기(가중치W)와 절편을 알아보는 모델
            - MAE : 평균 절대 오차
            - MSE : 평균 제곱 오차
            - RMSE : 평균 제곱근 오차
            - R2-score : 결정계수, 적합여부( 1에 가까울수록 잘 만들어진 모델)

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day57_ml_01.ipynb

### Streamlit 기초 실습
    - layout
    - cache
    - form

---

# 2026-07-30
### 빅데이터 분석 모델링
    - 의사결정나무
        - 질문에 따라 판단(스무고개)
        - 최상위 루트부터 분할 (루트 -> 분할 -> 분할..)
        - 깊이가 깊어지면 과접합 발생 위험 증가
            - 깊이가 없거나 깊이 2이 성능이 서로 비슷하면 얕은 모델을 우선
        - 분류 / 회기 둘 다 가능

    - 랜덤포레스트(데이터 무작위 복원추출 -> 분할마다 특성도 무작위로 일부만 사용하여 여러 개 만듬 -> 평균/다수결로 예측)
        - 단일 나무보다 과적합에 강함
        - 개별 나무를 사람이 읽고 설명하기는 어려워진다는 트레이드오프가 있다.
        - '여러 사람에게 물어보고 다수결로 정한다'라는 비유
        - 분류 / 회귀 둘 다 가능
        - 분산 처리(배깅) 다수결(보팅)

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day58_ml_02.ipynb

### Streamlit 기초 실습
    - from
    - state
    - state_callback

---

# 2026-07-31
### 빅데이터 분석 모델링
    - 로지스틱 회귀
        -0~1사이의 확률을 출력 -> 임계값으로 잘라 참(1)/거짓(2)으로 분류
    - 혼동 행렬
        - TP : 실제 이탈을 이탈로 정확히 맞췄다
        - TN : 실제 비이탈을 비이탈로 정확히 맞췄다
        - FP : 실제 비이탈을 이탈로 잘못 예측
        - FN : 실제 이탈을 비이탈로 잘못 예측
    - k-means clustering
        - 중심점을 무작위로 놓는다 -> 가까운 점들을 그 중심에 배정 -> 배정된 점들의 평균으로 중심을 다시 계산 -> 반복

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/day59_ml_03.ipynb

### 팀 프로젝트
    - CCTV 정리

---

# 2026-08-03
### 통신 고객 이탈 모델을 학습하고 평가, 결과와 모델 저장(train.py)

### train.py로 만든 churn_model.joblib를 실제로 사용하는 사용자화면 코드

    https://github.com/TaeGaori/DATA_ANAYSIS/blob/main/train.py

### SQLD 시험 공부

---

# 2026-08-04
### 빅데이터분석모델링 TEST

    https://github.com/TaeGaori/DATA_ANAYSIS/tree/main/12_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D%EB%AA%A8%EB%8D%B8%EB%A7%81_%ED%83%9C%EB%91%90%ED%98%81

### 빅분기 실습 문제 (챕터 2-2)

    https://github.com/TaeGaori/BIGBUNGI/tree/main/part2_2_p224

### SQLD 시험 공부

---

# 2026-08-05
### 빅분기 실습 문제(챕터 2-4, 2-8)

    https://github.com/TaeGaori/BIGBUNGI/tree/main/part2_4_p264

    https://github.com/TaeGaori/BIGBUNGI/tree/main/part2_8_p332

---

# 2026-08-06
### 스트림릿으로 만드는 대구 지하철 승하차 통합 대시보드

    https://subwayapp-gaori.streamlit.app/

### 빅분기 실습 문제(머신러닝 실습(회귀))

---

# 2026-08-07
### 대구 지하철 승하차 통합 대시보드 마무리 -> 스트립릿과 연결

    https://subwayapp-gaori.streamlit.app/

### 빅분기 실습 문제 (챕터 3-1, 3-2)

    https://github.com/TaeGaori/BIGBUNGI/tree/main/part3_1_p357

    https://github.com/TaeGaori/BIGBUNGI/tree/main/prat3_2_p376
    
### SQLD 시험 공부
 
---

# 2026-08-10
### JWT : 클라이언트가 서명된 토큰을 보관하고, 서버는 서명을 검증

    https://github.com/TaeGaori/fastapi_2026/tree/main/todo

### SQLD 시험 공부

---

# 2026-08-11
### 데이터 모델링 TEST

    https://github.com/TaeGaori/DATA_ANAYSIS/tree/main/13_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D%EC%8B%9C%EC%8A%A4%ED%85%9C%EA%B0%9C%EB%B0%9C_%ED%83%9C%EB%91%90%ED%98%81

### SQLD 시험 공부

---

# 2026-08-12
### To-do list(JWT)
    - models.py - 파이썬 클래스와 DB테이블을 매핑
    - main.py - JWT 인증 토큰 방식
    - database/db_connection.py - PostgreSQL DB 연결 설정 + 라우터에서 사용할 세션 의존성(get_session)제공
    - database/orm.py - 모든 ORM모델의 부모가 되는 Base클래스 정의
    - repositories/todo_repository.py - todo테이블에 대한 DB쿼리만 담당하는 계층
    - repositories/User_repository.py - repositories/User_repository.py
    - schema/response.py - 서버가 클라이언트(사용자)에게 "돌려주는" 데이터의 형태를 정의하는 파일
    - schema/request.py - 클라이언트가 서버로 보내는 데이터의 형태를 정의하는 파일

    https://github.com/TaeGaori/fastapi_2026/tree/main/todo_project

### SQLD 시험 공부

---

# 2026-08-13
### To-do list(JWT)
    - sevices/todo_service.py - Todo 관련 "업무 규칙"을 담당하는 계층
    - sevices/user_service.py - 회원가입/로그인/토근재발급/로그아웃의 업무 규칙을 담당하는 계층
    - auth/password.py - 비밀번호 해싱(암호화 저장) / 검증을 담당하는 모듈
    - auth/dependencies.py - 현재 로그인한 사용자의 id --> 라우터마다 반복하지 않도록 공용 의존성 함수를 정의
    - auth/jwt.py - JWT 발급/검증 모듈(Access Token/Refresh Token)
    - routers/user.py - 회원가입/로그인 토근재발급/로그아웃의 업무 규칙을 담당하는 계층
    - sevices/todo_service.py - Todo 관련 "업무 규칙"을 담당하는 계층 
    - sevices/user_service.py - 회원가입/로그인/토근재발급/로그아웃의 업무 규칙을 담당하는 계층

    (https://github.com/TaeGaori/fastapi_2026/tree/main/todo(old_version))

### 빅분기 실습 (fromula(수식) 작성 문법 정리)
    - ~(물결) : target ~ a
    - +(더하기) : target ~ a + b + c
    
### SQLD 시험 공부

---

# 2026-08-14
### To-do list(JWT)
    - routers/todo.py - HTTP 요청을 받고 응답을 돌려주는 것만 담당
    - schema/request.py - 클라이언트가 서버로 보내는 데이터의 형태를 정의하는 파일
    - schema/response.py - 서버가 클라이언트(사용자)에게 "돌려주는" 데이터의 형태를 정의하는 파일
    - streamlit_app.py - FastAPI Todo API를 호출해서 화면으로 보여주는 프론트엔드 (FastAPI와 동시에 실행)

### SQLD 시험 공부 

---

# 2026-08-18
### Todo_project_ML
    - Todo 제목 텍스트로 카테고리를 분류하는 모델
    - FastAPI서버와 완전 분리된 별도 스크립트

    https://github.com/TaeGaori/fastapi_2026/tree/main/Todo_project_ML/ml

### 빅분기 실습(카이지곱 검정)
    - 적합도 검정
        - observed: 관측된 빈도 리스트（배열） 
        - expected: 기대 빈도 리스트（배열） , 주어지지 않으면 모든 카테고리의 관측 빈도가 균일하고 관측 빈도의 평균으로 주어진다고 가정함 
        - ddof 자유도 조정 , 기본값 0 
        - axis: 축 , 기본값0 
    - 독립성 검정
        - table: 교차표(Contingency Table) 데이터（2차원 형태） 
        - correction: 
    - 동질성 검정
        - table: 교차표(Contingency Table) 데이터（2차원 형태） 
        - correction: 연속성 보정 여부 , 기본값은 True , "연속정 수 정을 하지 않는다" 라는 조건이 있다면 False로 설정한다． 

    https://github.com/TaeGaori/BIGBUNGI/blob/main/part3_3_p386/ch3.ipynb

### SQLD 시험 공부

---

# 2026-08-19
### 빅데이터 시각화 TEST

    (https://github.com/TaeGaori/fastapi_2026/tree/main/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0/14_%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B6%84%EC%84%9D%EA%B2%B0%EA%B3%BC%EC%8B%9C%EA%B0%81%ED%99%94_%ED%83%9C%EB%91%90%ED%98%81)

### Todo_project_ML
    - sevices/category_service.py - 학습된 ML 모델(파이프라인 객체)을 감싸서 "제목 문자열 -> 카테고리 문자열" 예측만 담당하는 아주 얇은 계층
    - sevices/todo_service.py - category관련 코드 추가 
    - routers/ml.py - 카테고리 예측 모델의 "정확도"를 확인할 수 있는 모니터링 전용 엔드포인트
    - schema/response.py- class ModelAccuracyResponse(BaseModel) 추가
    - ml/retrain.py - 사용자가 실제로 수정한 카테고리(final_category)를 새 학습 데이터로 삼아 모델로 재학습

    (https://github.com/TaeGaori/fastapi_2026/tree/main/todo_project)

### SQLD 시험 공부

---

# 2026-08-20
### Todo_project_ML
    - Streamlit -> ML관련 코드 추가

    (https://github.com/TaeGaori/fastapi_2026/tree/main/Todo_project_ML)

### 예광탄 방식을 활용한 책장 코드

---

# 2026-08-21
### 우리 집 책장
    - Version 0 - 기본 세팅 
    - Version 1 - 관통로 확인
    - Version 2 - 진짜 이미지인지 검증
    - Version 3 - OCR로 ISBN후보 추출

### SQLD 시험 공부

---

# 2026-08-25
### 우리 집 책장
    - Version 4 - 국립중앙도서관 소장자료 검색 API 버전
    - Version 5 - 국립중앙도서관 소장자료 검색 중복확인 및 책 표지 등록

### 펭귄 종 예측 미니프로젝트 (모델링 + API)   *개별

### 팀 프로젝트(26년 월드컵 선수 정보)

---

# 2026-08-26
### 펭귄 종 예측 미니프로젝트 (모델링 + API)   *개별

### 팀 프로젝트(26년 월드컵 선수 정보)

### Docker 기본 세팅 및 기초 공부
    - ISBN 추출

---

# 2026-08-27
### 팀 프로젝트(26년 월드컵 선수 정보)

    (https://github.com/TaeGaori/fastapi_2026/tree/main/worldcup)
### Docker(home_library_v0)
    - ISBN 추출

    (https://github.com/TaeGaori/fastapi_2026/tree/main/home_library_v0)
### Docker(home_library_v1)
    - ISBN 추출 + DB 저장

    (https://github.com/TaeGaori/fastapi_2026/tree/main/home_library_v1)

---

# 2026-08-28
### 팀 프로젝트(26년 월드컵 선수 정보) TEST

    (https://github.com/TaeGaori/fastapi_2026/tree/main/%EB%B9%85%EB%8D%B0%EC%9D%B4%ED%84%B0/15_%EC%84%9C%EB%B2%84%ED%94%84%EB%A1%9C%EA%B7%B8%EB%9E%A8%EA%B5%AC%ED%98%84_3%EC%A1%B0)
    
### Docker(home_library_v2)
    - 중복 등록 응답을 에러가 아닌 메세지로 개선

    (https://github.com/TaeGaori/fastapi_2026/tree/main/home_library_v2)


---

# 2026-08-30
### 펭귄 종 예측 미니프로젝트 (모델링 + API)   *개별
    (https://github.com/TaeGaori/fastapi_2026/tree/main/penguin-project)

---

# 2026-08-31
### Docker(home_library_v3) 실행 환경 통일하기
    - FastAPI(api) + Streamlit(web) + PostgreSQL(db)
        
    (https://github.com/TaeGaori/fastapi_2026/tree/main/home_library_v3)
