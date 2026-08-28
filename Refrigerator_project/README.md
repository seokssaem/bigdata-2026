# 🥬 냉장고 식재료 관리 시스템

## 1. 프로젝트 소개

냉장고에 보관 중인 식재료의 정보를 PostgreSQL 데이터베이스에 저장하고 FastAPI를 이용하여 관리하는 프로젝트입니다.

식재료의 이름, 카테고리, 수량, 구매일, 유통기한, 보관방법 등의 정보를 등록하고 조회할 수 있으며, 수정 및 삭제 기능을 제공합니다.

또한 Streamlit을 이용하여 식재료 현황을 시각적으로 확인할 수 있도록 구성하였습니다.

특히 유통기한이 지난 식재료와 유통기한이 임박한 식재료를 구분하여 보여주고, 카테고리와 보관방법에 따른 식재료 현황을 차트로 확인할 수 있습니다.

---

## 2. 프로젝트 목표

* PostgreSQL 데이터베이스와 FastAPI 연동
* SQLAlchemy ORM을 이용한 데이터 관리
* 식재료 CRUD API 구현
* 검색 및 필터 기능 구현
* 페이지네이션 구현
* CSV 파일을 이용한 식재료 대량 등록
* 유통기한 만료 및 임박 식재료 확인
* Streamlit을 이용한 데이터 시각화
* 팀원 간 역할 분담을 통한 협업 프로젝트 수행

---

## 3. 개발 환경

| 구분            | 사용 기술       |
| ------------- | ----------- |
| Language      | Python      |
| Backend       | FastAPI     |
| Database      | PostgreSQL  |
| ORM           | SQLAlchemy  |
| Validation    | Pydantic    |
| Frontend      | Streamlit   |
| Data          | Pandas, CSV |
| HTTP 통신       | Requests    |
| API Test      | Swagger UI  |
| Collaboration | GitHub      |

---

## 4. 프로젝트 디렉터리 구조

```text
fridge_project/
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── TROUBLESHOOTING.md
│
├── routers/
│   └── ingredient.py
│
├── schema/
│   ├── request.py
│   └── response.py
│
├── frontend/
│   └── streamlit.py
│
└── data/
    └── upload.csv
```

### 주요 파일 설명

| 파일                      | 역할                               |
| ----------------------- | -------------------------------- |
| `main.py`               | FastAPI 애플리케이션 실행 및 라우터 등록       |
| `database.py`           | PostgreSQL 연결 및 SQLAlchemy 세션 관리 |
| `models.py`             | SQLAlchemy ORM 모델 정의             |
| `routers/ingredient.py` | 식재료 관련 API 엔드포인트 구현              |
| `schema/request.py`     | 식재료 등록 및 수정 요청 모델                |
| `schema/response.py`    | API 응답 모델                        |
| `frontend/streamlit.py` | Streamlit 사용자 화면 및 데이터 시각화       |
| `data/upload.csv`       | 식재료 대량 등록용 CSV 데이터               |
| `requirements.txt`      | 프로젝트 실행에 필요한 Python 라이브러리        |
| `TROUBLESHOOTING.md`    | 프로젝트 진행 과정에서 발생한 문제와 해결 과정       |

---

## 5. 데이터베이스 구조

### `ingredients` 테이블

| 필드                | 설명        |
| ----------------- | --------- |
| `id`              | 식재료 고유 번호 |
| `name`            | 식재료 이름    |
| `category`        | 식재료 카테고리  |
| `quantity`        | 식재료 수량    |
| `purchase_date`   | 구매일       |
| `expiration_date` | 유통기한      |
| `storage_method`  | 보관방법      |
| `created_at`      | 데이터 생성일시  |

---

## 6. 주요 기능

### 6.1 식재료 등록

새로운 식재료를 PostgreSQL 데이터베이스에 등록합니다.

등록 정보:

* 식재료 이름
* 카테고리
* 수량
* 구매일
* 유통기한
* 보관방법

### 6.2 식재료 목록 조회

PostgreSQL에 저장되어 있는 식재료 목록을 조회합니다.

식재료 ID 순서대로 조회하며 `skip`, `limit` 값을 이용하여 페이지네이션을 처리할 수 있습니다.

### 6.3 식재료 검색 및 필터

다음 조건으로 식재료를 검색하거나 필터링할 수 있습니다.

* 식재료 이름: 부분 문자열 검색 지원 (이름에 포함된 단어로 검색 가능)
* 카테고리: 정확히 일치하는 카테고리로 필터링
* 보관방법: 정확히 일치하는 카테고리로 필터링

### 6.4 식재료 단건 조회

식재료 ID를 이용하여 특정 식재료의 상세 정보를 조회합니다.

존재하지 않는 ID를 요청하면 `404 Not Found` 오류를 반환합니다.

### 6.5 식재료 수정

`PATCH` 방식을 사용하여 기존 식재료 정보 중 변경하려는 항목만 수정할 수 있습니다.

### 6.6 식재료 삭제

식재료 ID를 이용하여 데이터를 삭제할 수 있습니다.

삭제가 완료되면 `204 No Content` 상태 코드를 반환합니다.

### 6.7 CSV 대량 등록

CSV 파일을 업로드하여 여러 개의 식재료 정보를 한 번에 PostgreSQL 데이터베이스에 등록할 수 있습니다.

CSV 데이터 예시:

```text
식재료,분류,수량,구매일,유통기한,보관
우유,유제품,1개,8/25,8/30,냉장
사과,과일,5개,8/25,9/1,냉장
```

CSV 파일의 날짜 정보를 변환하여 저장하며, 필수 데이터가 누락되거나 날짜 형식이 올바르지 않은 행은 건너뛰도록 처리하였습니다.

---

## 7. API 목록

| Method | Endpoint                       | 기능              |
| ------ | ------------------------------ | --------------- |
| GET    | `/`                            | API 서버 실행 상태 확인 |
| POST   | `/ingredients`                 | 식재료 단건 등록       |
| GET    | `/ingredients`                 | 식재료 목록 조회       |
| GET    | `/ingredients/{ingredient_id}` | 식재료 단건 조회       |
| PATCH  | `/ingredients/{ingredient_id}` | 식재료 부분 수정       |
| DELETE | `/ingredients/{ingredient_id}` | 식재료 삭제          |
| POST   | `/ingredients/upload`          | CSV 식재료 대량 등록   |

### 목록 조회 Query Parameter

`GET /ingredients`에서는 다음 파라미터를 사용할 수 있습니다.

| Parameter        | 기능        |
| ---------------- | --------- |
| `keyword`        | 식재료 이름 키워드 검색 |
| `category`       | 카테고리 필터   |
| `storage_method` | 보관방법 필터   |
| `skip`           | 조회 시작 위치  |
| `limit`          | 조회 개수     |

---

## 8. Streamlit 주요 기능

Streamlit 화면에서는 다음 기능을 제공합니다.

### 홈 대시보드

* 전체 식재료 수
* 유통기한 만료 식재료 수
* 3일 이내 유통기한 임박 식재료 수
* 보관 여유 식재료 수
* 유통기한 상태별 식재료 차트
* 유통기한 만료 식재료 표시
* 유통기한 임박 식재료 표시

### 식재료 현황

* 카테고리별 식재료 수
* 보관방법별 식재료 수
* 차트를 이용한 데이터 시각화

### 식재료 목록

* 전체 식재료 조회
* 식재료 이름 검색
* 카테고리 필터
* 보관방법 필터
* 페이지네이션

### 식재료 등록

Streamlit 화면에서 새로운 식재료를 입력하여 FastAPI를 통해 PostgreSQL에 등록할 수 있습니다.

### 식재료 수정 및 삭제

등록되어 있는 식재료를 선택하여 정보를 수정하거나 삭제할 수 있습니다.

### CSV 업로드

CSV 파일을 선택하여 여러 개의 식재료 정보를 한 번에 등록할 수 있습니다.

---

## 9. 프로젝트 실행 방법

### 1. 가상환경 활성화

Windows Git Bash 기준:

```bash
source .venv/Scripts/activate
```

### 2. 필요한 라이브러리 설치

```bash
python -m pip install -r requirements.txt
```

### 3. PostgreSQL 실행

PostgreSQL 서버를 실행하고 프로젝트에서 사용하는 데이터베이스가 생성되어 있는지 확인합니다.

### 4. FastAPI 실행

프로젝트 최상위 디렉터리에서 실행합니다.

```bash
uvicorn main:app --reload
```

FastAPI 서버가 정상적으로 실행되면 기본 주소에서 API 서버 상태를 확인할 수 있습니다.

### 5. Swagger UI 확인

FastAPI 서버 실행 후 웹 브라우저에서 `/docs`에 접속합니다.

Swagger UI에서 식재료 등록, 조회, 수정, 삭제, 검색 및 CSV 업로드 API를 직접 테스트할 수 있습니다.

### 6. Streamlit 실행

프로젝트 최상위 디렉터리에서 다음 명령을 실행합니다.

```bash
streamlit run frontend/streamlit.py
```

FastAPI 서버와 Streamlit을 동시에 실행해야 정상적으로 데이터를 조회하고 관리할 수 있습니다.

---

## 10. 팀원 역할
|팀원| 담당 영역|주요 역할 및 작업 내용|
|-----|-----|-----|
| **김시현**   | 데이터 · PostgreSQL | PostgreSQL 데이터베이스 연결 환경 구축, SQLAlchemy 기본 설정, `ingredients` 테이블 초기 ORM 설계, 식재료 CSV 데이터 준비 및 대량 적재 기능 구현, 기본 목록 조회 및 카테고리 필터 기능 구현, 데이터 적재 과정의 컬럼 및 NOT NULL 문제 해결 |
| **노가희**   | FastAPI 백엔드      | FastAPI 프로젝트 구조 정리 및 Router 기반 모듈화, SQLAlchemy ORM 모델 개선, 구매일·유통기한 `Date` 타입 적용, 보관방법 필드명 수정, Request/Response Schema 분리, CRUD 및 검색·필터·페이지네이션·예외처리 기능 정비          |
| **홍은경**   | Streamlit · 시각화  | FastAPI와 Streamlit 연동, 냉장고 현황 대시보드 구현, 유통기한 만료·임박 식재료 관리, 카테고리별·보관방법별 차트 구현, 검색·필터·페이지네이션 화면 구현, 식재료 등록·수정·삭제 및 CSV 업로드 UI 구현                                     |
| **공동 작업** | 테스트 · 문서화        | Swagger UI API 테스트, PostgreSQL·FastAPI·Streamlit 연동 테스트, 오류 수정 및 최종 기능 점검, GitHub 소스 관리, `README.md`·`TROUBLESHOOTING.md` 작성                    |

---

## 11. 주요 문제 해결 경험

프로젝트를 진행하면서 다음과 같은 문제를 경험하고 해결하였습니다.

* PostgreSQL 테이블과 SQLAlchemy 모델 간 필드명 불일치
* `stroage_method` 오타 문제
* CSV 컬럼명과 ORM 필드 간 매핑 문제
* 구매일 및 유통기한 데이터 타입 문제
* NOT NULL 컬럼 데이터 누락 문제
* CSV 날짜 형식 변환 문제
* CSV 업로드 후 목록에 데이터가 보이지 않는 문제 (조회 범위 고정)
* 실행 중인 Streamlit 파일 불일치로 메뉴 화면이 겹쳐 보이는 문제
* 페이지네이션 데이터와 전체 통계 데이터 범위가 달라지는 문제
* 유통기한 정보를 직관적으로 파악하기 어려운 문제
* 유통기한이 지난 식재료 삭제 시 화면 이동이 번거로운 문제
* 사이드바 Radio 메뉴의 사용성 문제
* 페이지 이동 버튼 크기·간격 문제
* 데이터 시각화 위치로 인한 화면 복잡도 문제

자세한 문제 발생 원인과 해결 과정은 `TROUBLESHOOTING.md`에 기록합니다.

---

## 12. 프로젝트 결과

FastAPI, PostgreSQL, SQLAlchemy를 이용하여 실제 식재료 데이터를 관리하는 FAST API를 구현하였습니다.

단순 CRUD에서 끝나지 않고 검색, 필터, 페이지네이션, CSV 대량 등록 기능을 추가하였으며 Streamlit을 이용하여 사용자가 직접 식재료를 등록하고 관리할 수 있는 화면을 구현하였습니다.

또한 유통기한 데이터를 활용하여 만료 및 임박 식재료를 구분하고 다양한 통계와 차트로 냉장고의 식재료 현황을 확인할 수 있도록 구성하였습니다.
