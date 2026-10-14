# 학습일지

작성자: 태두혁

---

## 2026-06-15

### FastAPI 블로그 포스트 검색·생성·수정·삭제 기능 복습
### HTML/CSS 수업 내용 복습

---

## 2026-06-16

### FastAPI 오늘 뭐먹지?? 복습

---

## 2026-06-17

### 토이 프로젝트: 게임 캐릭터 만들기

---

## 2026-06-18

### FastAPI routers(회원가입) 복습

---

## 2026-06-17

### HTML + CSS를 활용한 대시보드 웹페이지 만들기 복습

---

## 2026-06-22

### HTML 애니메이션 활용

- translate: 현재 위치에서 x, y축으로 이동
- scale: 확대 또는 축소
- rotate: 중심축 기준으로 회전
- perspective: 3D 변형 시 입체감 부여
- skew: 비틀거나 기울임
- product
- animation: 시간에 따라 변화시킴

---

## 2026-06-23

### HTML 총정리 (원두 사이트)

---

## 2026-06-24

### SQL 기초 공부

```sql
SELECT   컬럼명      -- 1. 뭘 볼지
FROM     테이블명    -- 2. 어디서
WHERE    조건        -- 3. 어떤 조건으로
GROUP BY 그룹기준    -- 4. 어떻게 묶을지
HAVING   그룹조건    -- 5. 묶은 결과 조건
ORDER BY 정렬기준    -- 6. 어떻게 정렬할지
LIMIT    숫자        -- 7. 몇 개만 볼지
```

- 사용하지 않는 절은 생략할 수 있지만, 사용할 때는 위 순서를 지킨다.

### HTML 원두 사이트를 활용한 나만의 페이지 편집

---

## 2026-06-25

### SQLD: JOIN으로 두 테이블 연결하기

---

## 2026-06-26

### SQLD: 기출문제 실습 및 연습문제 풀이

---

## 2026-06-29

### FastAPI 복습

- CRUD: 데이터를 다루는 4가지 기본 동작
    - Create (생성): POST(FastAPI) / INSERT(SQL) → 예) 회원가입, 글 작성
    - Read (조회): GET(FastAPI) / SELECT(SQL) → 예) 목록 보기, 상세 보기
    - Update (수정): PUT·PATCH(FastAPI) / UPDATE(SQL) → 예) 정보 수정
    - Delete (삭제): DELETE(FastAPI) / DELETE(SQL) → 예) 회원 탈퇴, 글 삭제
- sql_databases: User + Item, 1:N 관계 CRUD
    - 공식 FastAPI 튜토리얼 예제를 PostgreSQL로 변환한 버전
    - User(사용자)가 여러 개의 Item(아이템)을 소유하는 1:N 구조
    - `crud.py`를 별도로 분리하여 DB 조작 로직과 라우터 로직을 나눔
- `__init__.py` 생성 이유: 오류 방지

---

## 2026-06-30

### 판다스로 엑셀 파일 읽기, 병합, 시각화

### FastAPI main 테스트

- pytest: 파이썬 표준 테스트 도구
- 파일과 함수 이름은 `test_`로 시작
- 권장사항: 테스트용 DB를 따로 만든다.
- 설치: `uv add pytest`

---

## 2026-07-01

### 데이터 수집 파이프라인 - CSV 파일 방식

- 전체 파이프라인 흐름
    1. 환경설정: 라이브러리 불러오기, 경로·DB URL 설정
    2. 수집: CSV 파일 읽기 (인코딩: 윈도 cp949)
    3. 변환: 파일에 따라 처리
    4. 파생컬럼(파생변수) 생성: 예) 시작시, 날짜, 요일코드, 주말여부
    5. 검증: 유효성 검증 리포트 출력
    6. DB 저장: PostgreSQL → subwaydb
    7. CSV 저장: output 폴더 안에 CSV 파일 저장 (utf-8)

### 응용: 공용주차장 CSV 컬럼 추출

---

## 2026-07-02

### 데이터 수집 파이프라인 - API 방식

- 전체 파이프라인 흐름
    1. 공공데이터포털에서 원하는 API 활용 신청
    2. API 키 준비(.env), 기본 설정 준비(dotenv)
    3. 수집: JSON 구조 확인, 전체 페이지 수집
    4. 판다스 데이터프레임 만들기
    5. 변환: 데이터 확인, 컬럼명, 자료형
    6. 파생컬럼(파생변수) 추가
    7. 데이터 검증 (생략 가능)
    8. DB 저장: pgAdmin에서 데이터베이스(busapidb) 생성 → 테이블 저장
    9. CSV 저장: bus_stop.csv, 인코딩 utf-8

### 응용: 정류소별 경유노선 API 조회

---

## 2026-07-03

### 데이터 수집 TEST - API 방식

- 검색 지역의 1등 당첨 상호명과 횟수를 수집한 뒤 DB에 저장

---

## 2026-07-06

### SQLAlchemy: 대체키 + UNIQUE 선언

```python
__table_args__ = (
    UniqueConstraint("컬럼1", "컬럼2", "컬럼3", name="제약조건이름"),
)
```

- `__table_args__`
    - 테이블의 부가 설정(제약조건, 인덱스 등)을 담는 클래스 속성
    - SQLAlchemy가 이름을 보고 자동 인식
    - 콤마를 붙여 튜플로 인식시켜야 함
- `UniqueConstraint("컬럼1", "컬럼2", ..., name="제약조건이름")`
    - 나열된 컬럼들의 조합이 테이블 전체에서 유일
    - `name=`은 필수가 아니지만, 에러가 나거나 제약조건을 참조해야 할 때가 많아 관례상 붙임

### 전체 파이프라인

1. 테이블 재설계
2. 기존 테이블을 삭제하고 재설계한 모델로 다시 생성
3. CSV → DB 배치 적재

---

## 2026-07-07

### SQLAlchemy: 자연키 + merge 선언

---

## 2026-07-08

### football SQLAlchemy 모델 정의

- 관계 정의 구분법
    - 1:N: 중간 테이블 불필요. ForeignKey만 있으며, 외래키가 있는 클래스가 N
    - N:M: 중간 테이블 필요. `secondary`가 있으며, 1:N은 생각할 필요 없음

---

## 2026-07-09

### football SQLAlchemy 테스트 코딩

### seed_postgres_basic.py

- `test_crud.py`는 CSV 파일을 직접 읽지 않음
- 따라서 테스트 전에 CSV 데이터를 PostgreSQL 테이블에 넣고 실행
- 실행 시 기존 테이블이 삭제되고 다시 만들어지므로, 중요한 데이터가 있다면 실행하지 않기

---

## 2026-07-10

### 데이터 저장 TEST

---

## 2026-07-13

### 만들어 둔 DB를 이용한 데이터 처리 시스템 개발

---

## 2026-07-14

### NCS 빅데이터 처리 시스템 개발 복습

- 원본 데이터 탐색
- 역별 인원 값 집계
- 시간대별 승차 인원 집계
- 날짜별 승·하차 집계

---

## 2026-07-15

### SQLAlchemy 2.0 버전으로 코드 변경

---

## 2026-07-16

### SQLAlchemy 2.0 버전으로 코드 마무리

### Streamlit 라이브러리 기초 실습

- 파이썬 코드만으로 웹페이지(대시보드, 데이터 시각화 등)를 쉽게 만들 수 있도록 도와주는 파이썬 라이브러리
- 위젯 단위(버튼 클릭, 슬라이더 이동, 제목 등)로 구성

---

## 2026-07-20

### 빅데이터 처리 시스템 개발 TEST

---

## 2026-07-21

### 분석 데이터 전처리

### Streamlit 실습

- multiselect
    - `st.multiselect()`: 여러 개의 선택지를 동시에 선택할 수 있는 입력 위젯
    - `correct`처럼 정답을 `set`으로 저장하면 순서와 상관없이 값 포함 여부만 비교할 수 있음
    - `set(fruits) == correct`로 사용자가 고른 값과 정답을 비교
- slider
    - 슬라이더로 값을 선택하는 위젯 (최소·최대 설정 가능)
    - `min_value=time(0)`: 선택 가능한 가장 이른 시간은 00:00
    - `max_value=time(23)`: 선택 가능한 가장 늦은 시간은 23:00
- input
    - `placeholder`: 입력창 안내 문구
    - `max_chars`: 최대 입력 글자 수 제한
    - `type='password'`: 입력값을 가림
- file uploader
    - `type='csv'`: 확장자 제한
    - `accept_multiple_files=False`: 한 번에 하나의 파일만 업로드 가능
    - `pd.read_csv(file)`로 바로 읽을 수 있음

---

## 2026-07-22

### API 문서화 (메타데이터 추가)

- 목적: 처음 보는 다른 개발자가 docs만 보고도 사용법을 이해할 수 있도록 추가 설명을 채운다.
- `FastAPI(...)` 생성자에 title / version / description 추가
    - Swagger UI 맨 위 소개 영역에 표시된다.
- 각 `@app.get(...)`에 summary / description / response_description 추가
    - Swagger UI에서 각 엔드포인트를 펼쳤을 때 보이는 설명이다.
- 함수 매개변수의 기본값을 `Query(...)`로 감싸 파라미터별 설명 추가
    - Swagger UI의 "Try it out" 화면에서 각 입력 칸 옆에 표시된다.
- `operation_id` / `tags` 추가
    - operation_id: 해당 API를 가리키는 고유한 이름
    - tags: Swagger UI에서 엔드포인트들을 그룹으로 묶어 보여주는 기준

### 데이터 타입 변환 & 결측치 처리 기초

- `apply(pd.to_numeric)`: 선택한 여러 열에 숫자 변환 함수를 한 번에 적용
- `dropna()`
    - 결측값이 있는 행을 제거
    - 가장 간단하지만 데이터가 많이 삭제될 수 있어 신중하게 사용
    - 결측치 비율이 매우 낮을 때만 권장
    - 기본값은 행 기준(`axis=0`), `axis=1`은 열(컬럼) 기준
- `fillna()`: 결측치를 다른 값으로 채움
- `mode()`
    - 해당 열에서 가장 자주 나온 값들을 리스트 형태로 반환
    - 최빈값이 여러 개여도 첫 번째 값을 가져오려면 `[0]`

---

## 2026-07-23

### 데이터 타입 변환 & 결측치 처리: CSV 파일로 실습

### FastAPI pytest 단위 테스트

- `test_crud.py`: `crud.py` 함수를 호출해 DB 조회 로직만 검증
- `test_main.py`: HTTP 요청을 흉내 내어 URL / 상태코드 / 응답 구조를 검증 → API 완성 여부 결정
- `TestClient`: uvicorn 서버를 띄우지 않고 앱을 호출하므로 빠르게 같은 결과를 확인할 수 있음

---

## 2026-07-24

### 조별 토이프로젝트 토의

### 인코딩

- 통계와 모델을 만들려면 Text(인간 언어)를 Number(숫자)로 통역해 주어야 한다.
- fit: 범주(문자열) 학습
- transform: 숫자 변환
- fit_transform: 학습과 숫자 변환을 한 번에 수행
- `pd.get_dummies()`: 판다스에서 원핫 인코딩
- `LabelEncoder`: 사이킷런으로 레이블 인코딩
- `.inverse_transform()`: 레이블 인코딩 역변환(디코딩)

### 스케일링

- 컬럼 간 숫자의 상대적 크기 차이로 생기는 문제를 해결하기 위한 과정
- 정규화와 표준화를 가장 많이 활용
- 사이킷런 라이브러리에 구현되어 있음
- MinMaxScaler = (df_num - df_num.min()) / (df_num.max() - df_num.min())

---

## 2026-07-27

### 왜도 `.skew()`

- 데이터 분포가 좌우 대칭에서 얼마나, 어느 방향으로 치우쳐 있는지를 나타내는 지표
- 왜도 = 0: 좌우 대칭 (정규분포처럼)
- 왜도 > 0: 양의 왜도, 오른쪽으로 긴 꼬리 (대부분의 값은 작은 쪽에 몰려 있고, 소수의 큰 값이 꼬리를 늘림)
- 왜도 < 0: 음의 왜도, 왼쪽으로 긴 꼬리 (대부분의 값은 큰 쪽에 몰려 있고, 소수의 작은 값이 꼬리를 늘림)

### 파생 변수 생성 및 스케일링

- `scale_cols = []` → `scaler = StandardScaler()` → `df[scale_cols] = scaler.fit_transform(df[scale_cols])`

### 공유자전거 대여 운영 데이터 전처리와 EDA 실습

---

## 2026-07-28

### 분석 데이터 전처리 TEST

### 탐색적 데이터 분석 TEST

---

## 2026-07-29

### 빅데이터 분석 모델링

- 입력(피처)과 정답(타겟)을 분리 → 훈련 데이터와 검증 데이터 나누기 (사이킷런 `train_test_split`)
- 선형 회귀 (LinearRegression)
    - 연속적인 숫자를 예측하는 모델
    - 최적의 직선을 찾는 방법론
    - 기울기(가중치 W)와 절편을 알아보는 모델
    - MAE: 평균 절대 오차
    - MSE: 평균 제곱 오차
    - RMSE: 평균 제곱근 오차
    - R2-score: 결정계수, 적합 여부 (1에 가까울수록 잘 만들어진 모델)

### Streamlit 기초 실습

- layout
- cache
- form

---

## 2026-07-30

### 빅데이터 분석 모델링

- 의사결정나무
    - 질문에 따라 판단 (스무고개)
    - 최상위 루트부터 분할 (루트 → 분할 → 분할 ...)
    - 깊이가 깊어지면 과적합 위험 증가
    - 깊이를 주지 않은 모델과 깊이 2인 모델의 성능이 비슷하면 얕은 모델을 우선
    - 분류 / 회귀 모두 가능
- 랜덤포레스트
    - 데이터를 무작위 복원추출 → 분할마다 특성도 일부만 무작위로 사용하여 나무를 여러 개 만듦 → 평균/다수결로 예측
    - 단일 나무보다 과적합에 강함
    - 개별 나무를 사람이 읽고 설명하기는 어려워진다는 트레이드오프가 있음
    - "여러 사람에게 물어보고 다수결로 정한다"는 비유
    - 분류 / 회귀 모두 가능
    - 분산 처리(배깅), 다수결(보팅)

### Streamlit 기초 실습

- form
- state
- state_callback

---

## 2026-07-31

### 빅데이터 분석 모델링

- 로지스틱 회귀
    - 0~1 사이의 확률을 출력 → 임계값으로 잘라 참(1)/거짓(0)으로 분류
- 혼동 행렬
    - TP: 실제 이탈을 이탈로 정확히 맞춤
    - TN: 실제 비이탈을 비이탈로 정확히 맞춤
    - FP: 실제 비이탈을 이탈로 잘못 예측
    - FN: 실제 이탈을 비이탈로 잘못 예측
- k-means clustering
    - 중심점을 무작위로 놓는다 → 가까운 점들을 그 중심에 배정 → 배정된 점들의 평균으로 중심을 다시 계산 → 반복

### 팀 프로젝트

- CCTV 정리

---

## 2026-08-03

### 통신 고객 이탈 모델 학습·평가, 결과와 모델 저장 (`train.py`)

### `churn_model.joblib`를 실제로 사용하는 사용자 화면 코드

### SQLD 시험 공부

---

## 2026-08-04

### 빅데이터 분석 모델링 TEST

### 빅분기 실습 문제 (챕터 2-2)

### SQLD 시험 공부

---

## 2026-08-05

### 빅분기 실습 문제 (챕터 2-4, 2-8)

---

## 2026-08-06

### Streamlit으로 만드는 대구 지하철 승하차 통합 대시보드

- https://subwayapp-gaori.streamlit.app/

### 빅분기 실습 문제 (머신러닝 실습: 회귀)

---

## 2026-08-07

### 대구 지하철 승하차 통합 대시보드 마무리 → Streamlit과 연결

- https://subwayapp-gaori.streamlit.app/

### 빅분기 실습 문제 (챕터 3-1, 3-2)

### SQLD 시험 공부

---

## 2026-08-10

### JWT

- 클라이언트가 서명된 토큰을 보관하고, 서버는 서명을 검증한다.

### SQLD 시험 공부

---

## 2026-08-11

### 데이터 모델링 TEST

### SQLD 시험 공부

---

## 2026-08-12

### To-do list (JWT)

- `models.py`: 파이썬 클래스와 DB 테이블을 매핑
- `main.py`: JWT 인증 토큰 방식
- `database/db_connection.py`: PostgreSQL DB 연결 설정 + 라우터에서 사용할 세션 의존성(`get_session`) 제공
- `database/orm.py`: 모든 ORM 모델의 부모가 되는 Base 클래스 정의
- `repositories/todo_repository.py`: todo 테이블에 대한 DB 쿼리만 담당하는 계층
- `repositories/User_repository.py`: 조회 저장만 하는 계층
- `schema/response.py`: 서버가 클라이언트(사용자)에게 돌려주는 데이터의 형태를 정의하는 파일
- `schema/request.py`: 클라이언트가 서버로 보내는 데이터의 형태를 정의하는 파일

### SQLD 시험 공부

---

## 2026-08-13

### To-do list (JWT)

- `services/todo_service.py`: Todo 관련 "업무 규칙"을 담당하는 계층
- `services/user_service.py`: 회원가입 / 로그인 / 토큰 재발급 / 로그아웃의 업무 규칙을 담당하는 계층
- `auth/password.py`: 비밀번호 해싱(암호화 저장) / 검증을 담당하는 모듈
- `auth/dependencies.py`: 현재 로그인한 사용자의 id를 라우터마다 반복하지 않도록 공용 의존성 함수를 정의
- `auth/jwt.py`: JWT 발급 / 검증 모듈 (Access Token / Refresh Token)
- `routers/user.py`: 회원가입 / 로그인 / 토큰 재발급 / 로그아웃의 업무 규칙을 담당하는 계층

### 빅분기 실습: formula(수식) 작성 문법 정리

- `~` (물결): `target ~ a`
- `+` (더하기): `target ~ a + b + c`

### SQLD 시험 공부

---

## 2026-08-14

### To-do list (JWT)

- `routers/todo.py`: HTTP 요청을 받고 응답을 돌려주는 것만 담당
- `schema/request.py`: 클라이언트가 서버로 보내는 데이터의 형태를 정의하는 파일
- `schema/response.py`: 서버가 클라이언트(사용자)에게 돌려주는 데이터의 형태를 정의하는 파일
- `streamlit_app.py`: FastAPI Todo API를 호출해 화면으로 보여주는 프론트엔드 (FastAPI와 동시에 실행)

### SQLD 시험 공부

---

## 2026-08-18

### Todo_project_ML

- Todo 제목 텍스트로 카테고리를 분류하는 모델
- FastAPI 서버와 완전히 분리된 별도 스크립트

### 빅분기 실습: 카이제곱 검정

- 적합도 검정
    - 관측된 빈도가 기대하는 분포(이론적 분포)와 일치하는지 검정
    - `observed`: 관측된 빈도 리스트(배열)
    - `expected`: 기대 빈도 리스트(배열). 주어지지 않으면 모든 카테고리의 관측 빈도가 균일하고 관측 빈도의 평균으로 주어진다고 가정함
    - `ddof`: 자유도 조정, 기본값 0
    - `axis`: 축, 기본값 0
- 독립성 검정
    - 두 범주형 변수가 서로 독립인지 검정
    - `table`: 교차표(Contingency Table) 데이터 (2차원 형태)
    - `correction`: 연속성 보정 여부, 기본값은 True. 자유도가 1인 2×2 표일 때만 적용됨
    - 반환값: 검정통계량(statistic), p-value, 자유도(dof), 기대 빈도(expected_freq)
- 동질성 검정
    - 여러 집단의 범주별 분포가 서로 같은지 검정
    - `table`: 교차표(Contingency Table) 데이터 (2차원 형태)
    - `correction`: 연속성 보정 여부, 기본값은 True. "연속성 수정을 하지 않는다"라는 조건이 있다면 False로 설정

### SQLD 시험 공부

---

## 2026-08-19

### 빅데이터 시각화 TEST

### Todo_project_ML

- `services/category_service.py`: 학습된 ML 모델(파이프라인 객체)을 감싸 "제목 문자열 → 카테고리 문자열" 예측만 담당하는 아주 얇은 계층
- `services/todo_service.py`: category 관련 코드 추가
- `routers/ml.py`: 카테고리 예측 모델의 정확도를 확인할 수 있는 모니터링 전용 엔드포인트
- `schema/response.py`: `ModelAccuracyResponse(BaseModel)` 클래스 추가
- `ml/retrain.py`: 사용자가 실제로 수정한 카테고리(`final_category`)를 새 학습 데이터로 삼아 모델 재학습

### SQLD 시험 공부

---

## 2026-08-20

### Todo_project_ML

- Streamlit에 ML 관련 코드 추가

### 예광탄 방식을 활용한 책장 코드

---

## 2026-08-21

### 우리 집 책장

- Version 0: 기본 세팅
- Version 1: 관통로 확인
- Version 2: 진짜 이미지인지 검증
- Version 3: OCR로 ISBN 후보 추출

### SQLD 시험 공부

---

## 2026-08-25

### 우리 집 책장

- Version 4: 국립중앙도서관 소장자료 검색 API 버전
- Version 5: 국립중앙도서관 소장자료 검색 중복 확인 및 책 표지 등록

### 펭귄 종 예측 미니프로젝트 (모델링 + API) *개별

### 팀 프로젝트 (26년 월드컵 선수 정보)

---

## 2026-08-26

### 펭귄 종 예측 미니프로젝트 (모델링 + API) *개별

### 팀 프로젝트 (26년 월드컵 선수 정보)

### Docker 기본 세팅 및 기초 공부

- ISBN 추출

---

## 2026-08-27

### 팀 프로젝트 (26년 월드컵 선수 정보)

### Docker (home_library_v0)

- ISBN 추출

### Docker (home_library_v1)

- ISBN 추출 + DB 저장

---

## 2026-08-28

### 15_서버프로그램구현 TEST

### Docker (home_library_v2)

- 중복 등록 응답을 에러가 아닌 메시지로 개선

---

## 2026-08-30

### 펭귄 종 예측 미니프로젝트 (모델링 + API) *개별

---

## 2026-08-31

### Docker (home_library_v3): 실행 환경 통일하기

- FastAPI(api) + Streamlit(web) + PostgreSQL(db)

---

## 2026-09-02

### Docker (home_library_v4)

- jinja2 템플릿 적용

---

## 2026-09-03

### Docker (home_library_v4)

- jinja2 템플릿 적용 (마무리)

### GitHub Actions 자동 배포

- README.md에 기초 이론 정리

---

## 2026-09-07

### 16_통합구현 TEST (Docker)

### 자율학습 (penguin_body_mass)

---

## 2026-09-08

### GitHub Actions

- CI 단계: 테스트 자동화
- Build 단계: Docker 이미지 자동 빌드
- DB 연동 CI

### 자율학습 (penguin_body_mass 마무리)

---

## 2026-09-09

### Git 브랜치 만들기

- 사진 인식(Vision LLM) 기능처럼 아직 검증되지 않은 새 기능을 추가할 때, main을 건드리지 않고 안전하게 실험할 수 있는 "나만의 작업 공간"을 만드는 방법 (확인 후 병합)

### langchain_practice

- `00_check_setup.py`: 설치 확인 + Gemini API key 연결 확인 테스트
- `01_hello_setup.py`: 가장 단순한 호출. 프롬프트 템플릿 없이 문자열 하나로 바로 질문

### penguin_body_mass 풀이

---

## 2026-09-10

### GitHub Actions

- AWS Lightsail 배포 실습

### 자율학습 (당뇨병 진단 예측)

---

## 2026-09-11

### 자율학습 (당뇨병 진단 예측 마무리)

---

## 2026-09-14

### 자율학습 (빅분기 실기문제)

### MLOps

- ML 서비스 전체 구조
    1. 데이터 준비: 인코딩, 전처리
    2. 모델 학습: Pipeline, XGBoost
    3. 모델 저장: pkl 파일
    4. API 서빙: FastAPI

---

## 2026-09-15

### 자율학습 (빅분기 실기문제)

### MLOps (대출)

- `app/models.py`: 학습된 대출 심사 모델의 로딩, 전처리, 추론을 캡슐화한 모듈
- `app/schema.py`: 대출 API 요청/응답의 데이터 계약을 정의하는 pydantic 스키마

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-1일차)

- YOLOv8 Quickstart 따라 하기 (설치, `yolo predict` / `yolo train` CLI로 감 잡기)

---

## 2026-09-16

### 자율학습 (빅분기 실기문제)

### MLOps (대출)

- `app/main.py`: 대출 승인 예측 모델을 HTTP API로 제공하는 FastAPI 애플리케이션

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-2일차)

- MLflow Tracking Quickstart 따라 하기 (`log_param`, `log_metric`, MLflow UI 확인)
- Roboflow Universe에서 데이터셋 선택·다운로드 (Drone-Data)
- Roboflow 데이터로 YOLOv8 전이학습 1차 시도, MLflow 로깅 연동

---

## 2026-09-17

### MLOps (대출)

- `app/main.py`: 모델 정보 엔드포인트와 `@app.post` 부분에 요청 추적용 메타데이터 추가
- `app/schema.py`: 모델 정보 스키마와 요청 추적용 확장 응답 스키마 추가
- `app/models.py`: 배치 예측용 메서드 추가
- `.dockerignore` 및 `Dockerfile` 작성 → Docker 컨테이너화

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-3일차)

- FastAPI 코드 작성
    - `models/`, `routers/`, `schemas/`, `database.py`
- `schema.sql`: 데이터베이스 AegisVision 드론 탐지 로그 저장용 스키마 작성

---

## 2026-09-18

### React 기초 수업

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-4일차)

- FastAPI 코드 작성 및 오류 수정
    - `services/`, `main.py`

---

## 2026-09-21

### MLOps (대출)

- 테스트 코드 기초: `test_api.py`

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-6일차)

- FastAPI 코드 추가 작성 마무리 및 오류 수정
    - `routers/metrics.py`, `routers/training.py`, `schemas/training.py`, `merge_training_history.py`

---

## 2026-09-22

### MLOps (대출)

- GitHub Actions 코드 작성
    - `.github/workflows/ci-service-a.yml`

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-7일차)

- Docker 컨테이너 코드 작성
    - `Dockerfile`, `docker-compose.yml`, `requirements.txt`

---

## 2026-09-23

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-8일차)

- Streamlit 코드 작성
    - `streamlit_app.py`, `Dockerfile.streamlit`, `requirements-streamlit.txt`

---

## 2026-09-28

### MLOps (대출)

- HTML 코드 작성

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-9일차)

- API Key, JWT 코드 작성
    - `core/`, `middleware/`, `models/audit.py`, `models/user.py`, `routers/auth.py`, `schemas/auth.py`, `services/user_service.py`, `Caddyfile`

---

## 2026-09-29

### MLOps (대출)

- 드리프트 감지와 재학습 코드 작성

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-10일차)

- 알람 경보 코드 작성
    - `services/threat_service.py`, `services/detection_service.py`, `models/detection.py`, `routers/alerts.py`
- 비디오 탐지 코드 작성
    - `services/video-inference.py`, `routers/video.py`

---

## 2026-09-30

### React 기초 공부

- 훅, 이벤트 처리, 리스트와 키

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-11일차)

- 방산 스타일 지표 코드 작성
    - `scripts/evaluate_defense_metrics.py`, `routers/defense_metrics.py`, `services/metrics_service.py`

---

## 2026-10-01

### React 기초 공부

- 폼, state 끌어올리기, 합성과 특수화

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-12일차)

- GitHub 저장소 전체 점검, README 작성

---

## 2026-10-02

### MLOps 실무를 위한 LLM API 서버 구축

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-13일차)

- 코드 전체 점검

---

## 2026-10-04

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-14일차)

- React 코드 작성
    - `src/lib/tabs.ts`, `src/components/Sidebar.tsx`, `App.tsx`, `frontend/.env.local`

---

## 2026-10-05

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-16일차)

- React 코드 작성
    - `ApiStatus.tsx`, `lib/api.ts`

---

## 2026-10-06

### GitHub Actions + AWS Lightsail 수동 배포

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-17일차)

- React 코드 작성
    - `src/lib/usePolling.ts`, `src/pages/Alerts.tsx`, `src/components/Stat.tsx`, `src/pages/Dashboard.tsx`, `src/components/CountBarChart.tsx`

---

## 2026-10-07

### GitHub Actions + AWS Lightsail 자동 배포, 서버 안 DB

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-18일차)

- React 코드 작성
    - `pages/Detect.tsx`, `pages/ModelInfo.tsx`, `pages/Training.tsx`

---

## 2026-10-08

### GitHub Actions + AWS Lightsail: ci.yml을 Compose 배포용으로 교체하고 push

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-19일차)

- React 코드 작성
    - `components/TrainingChart.tsx`, `pages/Video.tsx`
- Docker 배포 설정
    - `frontend/Dockerfile`, `frontend/nginx.conf`, `frontend/.dockerignore`, `.env.example`

---

## 2026-10-13

### 드론영상 기반 객체 탐지 MLOps 파이프라인 구축 (pp-20일차)

- 발표자료 제작
- Lightsail 서버용 .env 생성
