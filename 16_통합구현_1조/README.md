# KOBIS API 기반 영화 정보 및 즐겨찾기 서비스

## 1. 프로젝트 소개

영화진흥위원회 KOBIS Open API를 활용하여 영화를 검색하고, 원하는 영화의 상세정보를 저장하여 즐겨찾기와 메모를 관리할 수 있는 서비스이다.

초기에는 기존 Todo CRUD 구조를 재활용한 영화 리뷰 프로토타입으로 핵심 흐름을 검증하였다. 이후 영화 서비스에 적합하도록 데이터 모델과 프로그램 구조를 재설계하고, 영화 검색·상세정보 저장·즐겨찾기·메모 관리 기능을 추가하였다.

## 2. 프로젝트 목표

- 외부 Open API를 활용한 영화 데이터 수집 및 가공
- FastAPI와 PostgreSQL을 이용한 REST API 구현
- Streamlit을 이용한 사용자 화면 구성
- 영화 코드 기반 데이터 저장 및 중복 방지
- 계층 분리를 통한 유지보수성과 확장성 개선
- 프로토타입 검증 결과를 발전 버전에 반영

## 3. 개발 과정

### 3.1 초기 프로토타입

기존 Todo CRUD 구조를 활용하여 영화 리뷰 서비스의 핵심 흐름을 빠르게 구현하였다.

```text
KOBIS 영화 목록 조회
        ↓
영화 선택
        ↓
리뷰 작성
        ↓
FastAPI를 통한 PostgreSQL 저장
        ↓
리뷰 조회 및 삭제
```

프로토타입에서는 기존 `Todo.title` 컬럼에 영화 제목과 리뷰를 다음과 같이 함께 저장하였다.

```text
기생충 | 사회적 메시지와 배우들의 연기가 인상적이었다.
```

#### 프로토타입 구현 기능

- KOBIS 영화목록 조회 API 호출
- JSON 응답을 Pandas 데이터프레임으로 변환
- 영화 선택 및 리뷰 작성
- 리뷰 등록·조회·삭제
- Streamlit과 FastAPI 간 데이터 전달
- PostgreSQL 데이터 저장

### 3.2 프로토타입의 한계

- 영화 제목과 리뷰가 하나의 컬럼에 함께 저장됨
- 영화 코드, 감독, 배우, 장르 등의 정보를 구분하여 관리하기 어려움
- 동일한 영화 정보가 중복 저장될 가능성이 있음
- Todo의 `is_done` 필드가 영화 서비스 목적과 맞지 않음
- 검색과 상세정보 조회 기능이 부족함
- 기능 확장 시 하나의 파일에 로직이 집중될 가능성이 있음

### 3.3 발전 버전

프로토타입에서 확인한 한계를 바탕으로 영화 카탈로그와 즐겨찾기 중심의 서비스로 발전시켰다.

| 구분 | 프로토타입 | 발전 버전 |
|---|---|---|
| 데이터 모델 | Todo 재활용 | Movie, Actor, Director, Favorite 분리 |
| 영화 식별 방법 | 영화 제목 | KOBIS 영화 코드 |
| 데이터 저장 | 영화명과 리뷰 통합 | 영화 정보와 즐겨찾기 메모 분리 |
| 영화 정보 | 영화 목록 일부 | 영화 상세정보·배우·감독 저장 |
| 검색 | 단순 목록 출력 | 영화명·감독·개봉연도 검색 |
| 목록 처리 | 한 번에 출력 | 페이지네이션 적용 |
| 코드 구조 | 단순 CRUD | Router–Service–Repository 계층 분리 |
| API 키 | 코드에 직접 입력 | `.env` 환경변수로 관리 |

## 4. 주요 기능

### 영화 검색

- 영화명 검색
- 감독명 검색
- 개봉연도 범위 검색
- 페이지 단위 목록 조회
- 영화별 개봉일·장르·국가 정보 확인

### 영화 상세정보 저장

- KOBIS 영화 상세정보 API 호출
- 영화 코드 기반 기존 데이터 확인
- 신규 영화 정보 저장
- 감독 및 배우 정보 분리 저장
- 동일 영화의 중복 저장 방지

### 즐겨찾기 관리

- 영화 즐겨찾기 등록
- 동일 영화 중복 즐겨찾기 방지
- 즐겨찾기 목록 조회
- 영화별 메모 작성 및 수정
- 즐겨찾기 삭제

## 5. 기술 스택

| 구분 | 기술 |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Backend | FastAPI |
| ORM | SQLAlchemy |
| Database | PostgreSQL |
| External API | KOBIS Open API |
| Data Processing | Pandas |
| HTTP Client | Requests |
| Environment | python-dotenv |

## 6. 시스템 구조

```text
사용자
  ↓
Streamlit
  ↓
FastAPI Router
  ↓
Service
  ↓
Repository
  ↓
SQLAlchemy
  ↓
PostgreSQL

Streamlit ──→ KOBIS Open API
```

### 계층별 역할

- **Streamlit**: 검색 조건 입력, 영화 목록 표시, 즐겨찾기 및 메모 관리 화면을 제공한다.
- **Router**: HTTP 요청을 전달받고 적절한 상태 코드와 응답을 반환한다.
- **Service**: 데이터 존재 여부, 중복 등록, 예외 상황 등의 업무 규칙을 처리한다.
- **Repository**: SQLAlchemy를 이용하여 데이터 조회·저장·수정·삭제를 수행한다.
- **Model**: 영화, 배우, 감독, 즐겨찾기 테이블과 관계를 정의한다.
- **PostgreSQL**: 영화 상세정보와 즐겨찾기 데이터를 저장한다.

## 7. 데이터베이스 구성

### Movie

- KOBIS 영화 코드를 기준으로 영화 기본정보를 저장한다.
- 영화명, 개봉일, 상영시간, 장르, 국가, 관람등급 등을 관리한다.

### Actor

- 영화별 배우 정보를 저장한다.
- `movie_cd`를 통해 Movie 테이블과 연결한다.

### Director

- 영화별 감독 정보를 저장한다.
- `movie_cd`를 통해 Movie 테이블과 연결한다.

### Favorite

- 즐겨찾기한 영화와 사용자가 작성한 메모를 저장한다.
- `movie_cd`를 통해 Movie 테이블을 참조한다.

```text
Movie 1 ─── N Actor
Movie 1 ─── N Director
Movie 1 ─── N Favorite
```

## 8. 실행 방법

### 8.1 프로젝트 설치

```bash
git clone <저장소 URL>
cd <프로젝트 폴더>
pip install -r requirements.txt
```

### 8.2 환경변수 설정

프로젝트 루트에 `.env` 파일을 만들고 다음 값을 입력한다.

```env
KOBIS_API_KEY=발급받은_API_키
DATABASE_URL=postgresql+psycopg2://사용자명:비밀번호@localhost:5432/데이터베이스명
```

> `.env` 파일에는 API 키와 데이터베이스 비밀번호가 포함되므로 Git에 업로드하지 않는다.

### 8.3 백엔드 실행

```bash
uvicorn main:app --reload
```

FastAPI API 문서는 다음 주소에서 확인할 수 있다.

```text
http://127.0.0.1:8000/docs
```

### 8.4 Streamlit 실행

```bash
streamlit run streamlit_app.py
```

> 실제 프로젝트의 파일 위치가 다르면 `main:app`과 `streamlit_app.py` 경로를 프로젝트 구조에 맞게 수정한다.

## 9. 주요 예외 처리

| 상황 | 처리 방법 |
|---|---|
| 잘못된 검색 조건 | 요청값 검증 후 안내 메시지 반환 |
| KOBIS API 호출 실패 | 상태 코드 확인 및 오류 메시지 출력 |
| 검색 결과 없음 | 빈 목록 또는 사용자 안내 메시지 표시 |
| 이미 등록된 영화 | 영화 코드를 확인하여 중복 저장 방지 |
| 이미 등록된 즐겨찾기 | `409 Conflict` 반환 |
| 존재하지 않는 데이터 | `404 Not Found` 반환 |
| DB 연결 실패 | 연결 문자열과 PostgreSQL 실행 상태 확인 |

---

# 10. 조별 트러블슈팅

## 팀원 1 — `김기완`

### 문제 1 — CSV 적재 중 `StringDataRightTruncation` 에러

**증상**: `load_data.py`로 `kobis_movie_details_2025.csv`를 PostgreSQL에 적재하는 중
아래 에러가 발생하며 전체 트랜잭션이 롤백됨.

```
psycopg2.errors.StringDataRightTruncation: 오류: character varying(50) 자료형에 너무 긴 자료를 담으려고 합니다.
```

**원인**: `models.py`의 `watch_grade` 컬럼을 `String(50)`으로 만들었는데, 실제 데이터 중
등급 변경 이력이 여러 개 붙은 영화가 있어 50자를 초과함.

```
'95-86(고등학생이상관람가)|2017-MF00346(15세이상관람가)'
```

**해결**: `watch_grade` 컬럼 길이를 `String(300)`으로 늘림. 다만 이미 옛날 스키마로
생성된 빈 테이블은 `Base.metadata.create_all()`이 건드리지 않으므로, `DROP TABLE`로
기존 테이블을 지운 뒤 다시 적재해야 함.

```python
watch_grade: Mapped[str | None] = mapped_column(String(300), nullable=True)
```

**포인트**: 컬럼 길이는 샘플 몇 개만 보고 정하면 안 되고, 실제 데이터의 최대 길이
분포를 확인해야 한다는 걸 알게 됨. 또한 스키마를 고쳐도 이미 생성된 테이블에는
자동 반영되지 않는다는 것(`create_all()`은 "없으면 만든다"이지 "다르면 고친다"가
아님)도 확인함.

---

### 문제 2 — `ImportError: cannot import name 'MovieListResponse'`

**증상**: 조회 응답에 전체 개수(total)를 포함하는 기능이 추가된 뒤 서버를 켜니
아래 에러로 서버 자체가 안 켜짐.

```
ImportError: cannot import name 'MovieListResponse' from 'schema.response'
```

**원인**: `routers/movie.py`는 새로 만든 `MovieListResponse`를 사용하도록 이미
고쳐져 있었는데, 정작 그 클래스를 정의해야 할 `schema/response.py` 쪽 파일은
예전 버전 그대로 남아 있었음. "사용하는 쪽"만 반영되고 "정의하는 쪽"은 안 된 상태.

**해결**: `schema/response.py`에 `MovieListResponse` 클래스를 실제로 추가.

```python
class MovieListResponse(BaseModel):
    total: int
    items: list[MovieSummaryResponse]
```

**포인트**: 여러 파일이 서로 맞물려 있을 때, 한 파일만 반영되고 나머지를 놓치면
바로 이런 에러가 난다는 걸 확인함. 파일을 여러 개 동시에 고칠 땐 "이 이름을 쓰는
파일"과 "이 이름을 정의하는 파일"을 항상 같이 확인해야 함.

---

### 문제 3 — 성인물 필터링 후 페이지네이션이 부정확함

**증상**: 검색 결과 중 성인물 장르를 제외하고 나니 화면에 3개 정도만 남았는데,
실제로는 뒤에 더 많은 데이터가 있음에도 "다음" 버튼이 비활성화됨.

**원인**: "다음 페이지가 있는지"를 **필터링 후(성인물 제외 후)의 개수**로 판단하고
있었음. 예를 들어 12개 중 9개가 성인물이면 3개만 남는데, `3 < 12`라서 다음 버튼이
꺼지는 구조였음.

```python
# 잘못된 코드
if nav2.button('다음 ▶', disabled=len(movies) < 12):   # movies는 필터링 후 개수
```

**해결**: 화면에 보여줄 개수가 부족하면, 성인물을 걸러내고도 12개를 채울 때까지
KOBIS를 100개 단위로 반복 호출해서 캐시에 쌓아두는 방식으로 변경. "다음 페이지
있는지"도 캐시에 다음 몫이 실제로 쌓여 있는지로 정확히 판단하도록 수정.

**포인트**: 필터링(성인물 제외)이 들어가는 순간, 단순히 "가져온 개수"만으로
페이지네이션을 판단하면 안 된다는 걸 알게 됨. 필터링 전/후 개수를 구분해서
다뤄야 함.

---

### 문제 4 (기능 개선) — 즐겨찾기 삭제 시 확인 절차 없음

**증상**: "삭제" 버튼을 누르면 확인 절차 없이 즉시 `DELETE` 요청이 실행되어,
실수로 삭제할 위험이 있음.

**원인**: 버튼 클릭 핸들러 안에서 바로 `requests.delete(...)`를 호출하는 구조였음.

**해결**: `st.session_state.confirming_delete`라는 상태값을 추가해서, "삭제"
버튼은 확인 상태로만 전환하고, 그 상태일 때만 "네, 삭제합니다" 버튼이 나타나
실제 삭제 요청을 보내도록 2단계로 분리.

```python
if c3.button('삭제', key=f'del_fav_{f["id"]}'):
    st.session_state.confirming_delete = f['id']   # 아직 지우지 않음
    st.rerun()

if st.session_state.get('confirming_delete') == f['id']:
    st.warning(f'"{f["movie_nm"]}"을(를) 정말 삭제하시겠습니까?')
    if confirm_col.button('네, 삭제합니다', ...):
        requests.delete(f'{API_BASE}/favorites/{f["id"]}')
        ...
```

**포인트**: Streamlit은 버튼을 누를 때마다 스크립트 전체가 재실행되는 구조라서,
"삭제 확인"처럼 여러 단계를 거치는 동작은 `session_state`로 현재 상태를 기억해둬야
구현할 수 있다는 걸 알게 됨.

---

## 팀원 2 — `김나현`

### 1. PostgreSQL 드라이버 누락으로 인한 서버 실행 오류
### 문제 상황

FastAPI 서버를 실행하는 과정에서 다음 오류가 발생하였다.

```ModuleNotFoundError: No module named 'psycopg2'```

SQLAlchemy를 사용해 PostgreSQL에 연결하도록 설정했지만, 애플리케이션이 데이터베이스 드라이버를 불러오지 못해 서버가 정상적으로 시작되지 않았다.

### 원인 분석

데이터베이스 연결 주소에는 PostgreSQL의 psycopg2 드라이버를 사용하도록 지정되어 있었다.
```python
DATABASE_URL = (
    "postgresql+psycopg2://postgres:1234@localhost:5432/tododb"
)
```
하지만 현재 가상환경에는 psycopg2 패키지가 설치되어 있지 않았다. 또한 패키지를 설치하더라도 FastAPI를 실행하는 Python 환경과 패키지를 설치한 환경이 다르면 동일한 문제가 계속 발생할 수 있었다.

### 해결 과정

개발 환경에 바이너리 형태의 PostgreSQL 드라이버를 설치하였다.

uv를 사용하는 환경에서는 다음 명령어로 의존성을 추가하였다.

`uv add psycopg2-binary`

설치 이후 현재 Python 환경에서 정상적으로 불러올 수 있는지 확인하였다.

`python -c "import psycopg2; print(psycopg2.__version__)"`

그다음 동일한 가상환경에서 FastAPI 서버를 다시 실행하였다.

`uvicorn main:app --reload`

### 해결 결과
FastAPI 서버가 정상적으로 실행되었다.
SQLAlchemy를 통해 PostgreSQL에 연결할 수 있었다.
영화 리뷰의 등록·조회·삭제 기능을 테스트할 수 있었다.
패키지 설치뿐만 아니라 실행 환경의 일치 여부도 중요하다는 것을 확인하였다.

### 배운 점
데이터베이스 연결 오류가 발생하면 연결 문자열만 확인하는 것이 아니라 드라이버 설치 여부, 가상환경 활성화 여부, 패키지 설치 위치를 함께 점검해야 한다.

---

### 2. KOBIS API의 중첩 JSON 구조 처리 문제
### 문제 상황
영화진흥위원회 KOBIS의 영화목록 조회 API를 호출한 후 응답 데이터를 바로 데이터프레임으로 변환하였다.
```python
data = response.json()
df = pd.DataFrame(data)
```
그러나 영화 한 편이 한 행으로 출력되지 않고, 전체 응답 구조가 하나의 값처럼 표시되거나 원하는 영화 목록이 나타나지 않았다.

### 원인 분석

KOBIS API가 반환하는 JSON은 영화 목록이 최상위에 위치한 단순 리스트 구조가 아니었다.
```python
{
  "movieListResult": {
    "totCnt": 1000,
    "source": "영화진흥위원회",
    "movieList": [
      {
        "movieCd": "20183782",
        "movieNm": "기생충",
        "openDt": "20190530"
      }
    ]
  }
}
```
실제 영화 목록은 다음 경로에 저장되어 있었다.

`movieListResult → movieList`

따라서 전체 JSON을 그대로 데이터프레임으로 변환하는 것이 아니라 실제 목록에 해당하는 리스트를 먼저 추출해야 했다.

### 해결 과정

API 응답의 구조를 먼저 확인하였다.
```python
data = response.json()
st.json(data)
```
이후 실제 영화 목록을 추출하여 데이터프레임으로 변환하였다.
```python
movies = data["movieListResult"]["movieList"]
df = pd.DataFrame(movies)
```
Streamlit 화면에는 다음과 같이 출력하였다.
```python
st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
)
```
### 해결 결과
영화 한 편이 데이터프레임의 한 행으로 출력되었다.
영화 코드, 영화명, 영문명, 제작연도 등의 정보를 확인할 수 있었다.
API에서 받은 영화 목록을 선택 위젯과 연결할 수 있었다.
```python
movie_names = df["movieNm"].tolist()
selected_movie = st.selectbox("영화를 선택하세요", movie_names)
```
### 추가 예외 처리

API 키가 잘못되었거나 서버가 정상적인 JSON을 반환하지 않을 가능성도 고려할 수 있다.
```python
response = requests.get(API_URL, params=params, timeout=10)
response.raise_for_status()
data = response.json()
```
영화 데이터가 없는 경우도 처리할 수 있다.
```python
movies = (
    data.get("movieListResult", {})
    .get("movieList", [])
)

if not movies:
    st.warning("조회된 영화가 없습니다.")
else:
    df = pd.DataFrame(movies)
    st.dataframe(df)
```

### 배운 점

외부 API를 연동할 때는 데이터프레임 변환 코드를 먼저 작성하기보다 JSON의 계층과 데이터 타입을 확인한 후 필요한 목록의 경로를 찾아야 한다.

---

### 3. 기존 Todo 데이터 구조와 영화 리뷰 데이터의 불일치
### 문제 상황

프로토타입은 기존에 구현한 Todo CRUD 프로젝트를 영화 리뷰 서비스로 변경하여 제작하였다.

기존 Todo 모델은 다음과 같이 구성되어 있었다.
```
Todo
- id
- title
- is_done
```
하지만 영화 리뷰 서비스에서는 다음과 같은 정보가 필요했다.

- 영화 코드
- 영화 제목
- 리뷰 내용
- 별점
- 작성일

기존 모델에는 영화 제목과 리뷰를 각각 저장할 컬럼이 없었으며, is_done은 영화 리뷰 서비스와 관련 없는 필드였다.

### 원인 분석

프로토타입의 목표는 완성된 서비스를 만드는 것이 아니라 다음 핵심 흐름이 실제로 동작하는지 빠르게 확인하는 것이었다.
```
외부 영화 API 호출
→ 영화 선택
→ 리뷰 작성
→ FastAPI 전송
→ PostgreSQL 저장
→ 리뷰 조회 및 삭제
```
따라서 초기 단계부터 새로운 데이터베이스를 설계하기보다 기존 Todo API를 재사용하였다. 이로 인해 서비스의 목적과 데이터 구조 사이에 차이가 발생하였다.

### 해결 과정

영화 제목과 리뷰 내용을 하나의 문자열로 결합하여 기존 title 컬럼에 저장하였다.
```python
review_data = {
    "title": f"{selected_movie} | {review}"
}
```
저장 예시는 다음과 같다.
```
기생충 | 사회적 메시지와 배우들의 연기가 인상적이었다.
```
기존 Todo의 완료 여부는 프로토타입 화면에서 사용하지 않도록 제거하였다.

### 해결 결과
기존 API와 데이터베이스 구조를 크게 변경하지 않고 영화 리뷰 기능을 구현하였다.
영화 선택부터 리뷰 저장까지의 사용자 흐름을 빠르게 검증하였다.
새로운 테이블 설계에 들어가기 전에 외부 API와 백엔드 간 연동 가능성을 확인하였다.
프로토타입의 구조적 한계를 구체적으로 파악할 수 있었다.

### 남아 있는 한계

영화명과 리뷰를 하나의 문자열로 저장하기 때문에 다음과 같은 문제가 있었다.

- 영화 제목만 따로 검색하기 어렵다.
- 리뷰 내용만 수정하기 어렵다.
- 영화 코드 기반으로 동일 영화를 구분할 수 없다.
- 제목에 구분 문자 |가 포함되면 데이터를 정확하게 나누기 어렵다.
- 별점이나 작성일 같은 새로운 필드를 추가하기 어렵다.
- 같은 영화 정보가 리뷰마다 중복 저장될 수 있다.

### 발전 버전에 반영한 개선

프로토타입에서 발견한 문제를 바탕으로 영화 서비스에 적합한 테이블을 별도로 설계하였다.
```
Movie
- movie_cd
- movie_nm
- open_dt
- genre
- nation
- watch_grade

Favorite
- id
- movie_cd
- memo
```
영화 정보를 Movie에 한 번만 저장하고, 사용자가 작성한 메모나 즐겨찾기 정보는 Favorite에서 관리하도록 분리하였다.

### 배운 점

프로토타입에서는 핵심 기능 검증을 위해 기존 구조를 재사용할 수 있지만, 정식 서비스로 발전시킬 때는 서비스 목적에 맞는 데이터 모델로 재설계해야 한다.

---

### 4. 회원가입·로그인 기능이 프로토타입의 목적과 맞지 않은 문제
### 문제 상황

기존 Todo 프로젝트에는 다음과 같은 사용자 인증 기능이 포함되어 있었다.

- 회원가입
- 로그인
- JWT 토큰 발급
- 로그인 사용자 확인
- 사용자별 Todo 조회
- 로그아웃
- 인증 만료 처리

하지만 영화 조회와 리뷰 등록 흐름을 검증하는 프로토타입에서는 로그인 과정 때문에 핵심 기능을 테스트하기까지 거쳐야 하는 단계가 많았다.

### 원인 분석

기존 Todo 프로젝트는 여러 사용자가 자신의 할 일을 관리하는 구조였기 때문에 사용자 인증이 필요했다.
```
User 1 ─── N Todo
```
그러나 영화 리뷰 프로토타입의 목표는 사용자별 데이터 관리가 아니라 KOBIS API와 FastAPI, PostgreSQL, Streamlit의 연동을 확인하는 것이었다.

로그인 기능을 그대로 유지하면 다음 문제가 발생하였다.

- 영화 기능과 관련 없는 회원가입 과정이 필요했다.
- 모든 API 요청에 JWT 토큰을 전달해야 했다.
- 토큰이 만료되면 리뷰 기능도 테스트할 수 없었다.
- User 테이블과 user_id 외래키를 계속 관리해야 했다.
- 프로토타입의 핵심 기능보다 인증 코드의 비중이 커졌다.

### 해결 과정

프로토타입의 범위를 핵심 기능에 집중시키기 위해 사용자 인증 기능을 제거하였다.

### 백엔드에서 제거한 항목
- User 모델
- 회원가입 및 로그인 라우터
- 비밀번호 암호화 로직
- JWT 생성 및 검증
- get_current_user 의존성
- Todo의 user_id 외래키
- 사용자별 데이터 조회 조건

기존 코드는 인증된 사용자만 Todo를 조회하는 구조였다.
```python
@router.get("/todos")
def get_todos(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.query(Todo).filter(
        Todo.user_id == current_user.id
    ).all()
```
인증을 제거한 뒤에는 모든 리뷰를 바로 조회할 수 있도록 변경하였다.
```python
@router.get("/todos")
def get_todos(
    db: Session = Depends(get_db),
):
    return db.query(Todo).all()
```
### Streamlit에서 제거한 항목
- 로그인·회원가입 탭
- 이메일과 비밀번호 입력창
- 로그아웃 버튼
- 세션 토큰 관리
- Authorization 요청 헤더
- 로그인 만료 안내
- 로그인 성공 여부에 따른 화면 분기
- 데이터베이스 처리

코드에서 모델을 삭제하더라도 `create_all()`은 기존 데이터베이스의 테이블이나 컬럼을 자동으로 삭제하지 않는다.

따라서 기존 리뷰 데이터를 유지하면서 `user_id` 컬럼과 `user` 테이블을 제거하는 마이그레이션이 필요했다.
```sql
ALTER TABLE todo
DROP COLUMN IF EXISTS user_id;

DROP TABLE IF EXISTS "user";
```
실제 테이블명과 제약조건에 따라 외래키를 먼저 제거해야 할 수도 있다.

### 해결 결과
앱을 실행하면 로그인 화면 없이 바로 영화 리뷰 화면이 나타났다.
API 요청마다 토큰을 전달할 필요가 없어졌다.
영화 조회와 리뷰 CRUD 기능을 빠르게 테스트할 수 있었다.
프로토타입의 코드와 사용자 흐름이 단순해졌다.

### 트레이드오프

인증을 제거함으로써 개발과 테스트는 간단해졌지만 다음과 같은 한계가 생겼다.

사용자별 리뷰를 구분할 수 없다.
모든 사용자가 같은 리뷰 목록을 보게 된다.
작성자 권한을 확인할 수 없다.
실제 서비스에 배포하기에는 보안과 개인정보 관리가 부족하다.

### 배운 점

프로토타입에서는 검증할 핵심 기능과 직접 관련되지 않은 기능을 제외해 개발 범위를 조절할 수 있다. 다만 정식 서비스에서는 사용자 인증과 권한 관리를 다시 설계해야 한다.

---

### 팀원 3 — `김동욱`

## 문제 1 (기능 개선) — 개봉연도를 특정연도와 일치하는 결과만 조회가 가능

**증상**: 조회 페이지에서 개봉연도(`year`)를 하나만 입력해 조회할 수 있었고,
특정 연도 범위(예: 2020~2025)로 검색하는 기능이 없었음.

**원인**: `fetch_kobis_list` 함수에서 `openStartDt`와 `openEndDt`에 동일한
`year` 값을 그대로 넣는 구조였음.

**해결**: KOBIS `searchMovieList` API 문서를 확인해 `openStartDt`(조회시작
개봉연도)와 `openEndDt`(조회종료 개봉연도)가 각각 독립적인 파라미터라는 걸
확인하고, 입력값을 `start_year`, `end_year`로 분리해 각각 전달하도록 수정.

```python
if start_year:
    params['openStartDt'] = start_year
if end_year:
    params['openEndDt'] = end_year
```

**포인트**: 겉보기엔 같은 "연도 검색"이라도 단일 값과 범위 값은 요구되는 파라미터 구조가 다르다는 걸 확인함.

## 문제 2 (기능 개선) — 감독명으로 조회 추가

**증상**: 영화명으로만 검색할 수 있고, 감독명으로 조회하는 기능이 없음.

**원인**: KOBIS 요청 파라미터에 `directorNm`이 아예 포함되어 있지 않았음.

**해결**: 감독명 입력창(`director_nm`)을 추가하고, 값이 있을 때만
`directorNm` 파라미터로 KOBIS 요청에 포함하도록 수정.

```python
director_nm = col2.text_input('감독명 검색')
...
if director_nm:
    params['directorNm'] = director_nm
```

**포인트**: API에서 어떤 파라미터들을 지원하는지 확인하는 과정이 필요하다는 것을 알게 됨.

## 문제 3 (설계 개선) — 정적 데이터(2025년 CSV)에서 실시간 API 조회로 전환

**초기 설계**: 조회 화면이 `kobis_movie_details_2025.csv`로 미리 받아둔 2025년 영화 데이터만 대상으로 검색이 가능하고, 영화 목록을 추가할 수 있게 설계함.

**초기 구조**: KOBIS에서 미리 받아온 CSV(`kobis_movie_details_2025.csv`)를
`load_data.py`로 DB(`Movie` 테이블)에 적재해두고, 조회 화면은 그 DB를 SQL로 검색하는 방식이었음.

**수정**: DB 검색 대신 KOBIS `searchMovieList`/`searchMovieInfo` API를 실시간으로 직접 호출하도록 변경.

```python
def fetch_kobis_list(api_key, keyword, director_nm, start_year, end_year, page):
    """KOBIS 영화 목록 검색 (제목/감독명/개봉연도 범위 조건, 페이지네이션)"""
    params = {'key': api_key, 'curPage': page, 'itemPerPage': 12}
    if keyword:
        params['movieNm'] = keyword
    ...
    res = requests.get(KOBIS_LIST_URL, params=params)
    return res.json()['movieListResult']
```

**포인트**: 정적 데이터는 한정된 데이터이고, 계속 변하는 데이터를 서비스하려면 실시간으로 변하는 데이터를 담아야 한다는 것을 다시 상기함.

---

# 11. 조별 역할 분담

## 11.1 역할 분담표

| 팀원  | 담당 영역          | 주요 수행 내용  | 산출물  |
| --- | -------------- | ------------------------------------------------------------------------- | ----------------------- |
| 김기완 | 즐겨찾기 및 콘텐츠 필터링 | 삭제 전 재확인 기능과 영화 등급 기반 성인물 필터링을 적용함  | 삭제 확인 기능, 성인물 필터링       |
| 김나현 | 프로토타입 및 서비스 연동 | Todo CRUD를 영화 리뷰 서비스로 변경하고 KOBIS API, Streamlit, FastAPI, PostgreSQL을 연동함 | 프로토타입, API 연동 및 리뷰 CRUD |
| 김동욱 | 영화 조회 및 검색 개선  | 실시간 KOBIS API 활용 방안을 제안하고 감독명 조회와 개봉연도 범위 검색을 구현함  | 영화 검색 및 조건별 조회 기능       |


## 11.2 팀원별 상세 역할

## 조별 역할 분담

| 팀원  | 담당 영역          | 주요 수행 내용  |
| ---- | ------------------ | -------------- |
| 김기완 | 즐겨찾기 및 콘텐츠 필터링 | 즐겨찾기 삭제 전 재확인 기능을 추가하여 실수로 인한 삭제를 방지하였다. 영화 등급 정보를 활용한 성인물 필터링을 적용하고 예외 상황을 점검하여 서비스의 안전성과 사용성을 개선하였다. |
| 김나현 | 프로토타입 및 서비스 연동  | Todo CRUD를 영화 리뷰 서비스로 변경하고, KOBIS API와 Streamlit을 연동하였다. 회원가입·로그인 기능을 제거하였다.         |
| 김동욱 | 영화 조회 및 검색 개선  | 최신 영화 정보를 반영할 수 있도록 실시간 KOBIS API 활용 방안을 제안하였다. 감독명 조회와 개봉연도 범위 검색을 추가하여 영화 검색의 정확성과 편의성을 높였다.         |

### 김기완

* 즐겨찾기 삭제 전 재확인 기능을 추가하여 사용자의 실수를 방지하였다.
* 영화 등급을 활용한 성인물 필터링을 적용하였다.
* 삭제와 필터링 과정의 예외 상황을 점검하여 사용성을 개선하였다.
### 김나현
* Todo CRUD를 활용해 영화 리뷰 서비스 프로토타입을 구현하였다.
* KOBIS API 영화 데이터를 Streamlit 화면과 연동하였다.
* 회원가입·로그인 기능을 제거하고 영화 서비스에 맞게 구조를 개선하였다.
### 김동욱

* 실시간 KOBIS API를 활용하는 영화 조회 방식을 제안하였다.
* 감독명 조회와 개봉연도 범위 검색 기능을 추가하였다.
* 다양한 검색 조건을 적용하여 영화 조회의 정확성과 편의성을 높였다.


---

# 12. 향후 개선 방향

- 별도 `Review` 테이블을 추가하여 즐겨찾기 메모와 리뷰를 분리
- 영화별 별점, 리뷰 작성일, 평균 별점 제공
- 사용자 인증을 적용하여 개인별 즐겨찾기와 리뷰 관리
- 장르·국가·감독별 영화 추천 기능 구현
- 검색 및 즐겨찾기 데이터를 활용한 개인화 추천
- API 호출 실패 및 네트워크 오류 처리 강화
- Docker를 활용한 실행 환경 통일
- 테스트 코드와 자동화된 배포 과정 추가

## Review 테이블 확장 예시

```text
Review
- id
- movie_cd
- user_id
- content
- rating
- created_at
```

# 13. 프로젝트를 통해 배운 점

- 프로토타입을 먼저 구현하여 핵심 서비스 흐름을 빠르게 검증할 수 있었다.
- 프로토타입의 한계를 분석하면서 필요한 테이블과 관계를 구체화할 수 있었다.
- 외부 API의 중첩 JSON 구조를 분석하고 필요한 데이터를 추출하는 방법을 학습하였다.
- FastAPI, Streamlit, PostgreSQL을 연결하여 하나의 서비스 흐름을 구현하였다.
- 계층별 역할을 분리하면서 유지보수가 가능한 백엔드 구조를 이해하였다.
- 팀원별 문제 해결 과정을 공유하는 것이 전체 프로젝트의 완성도를 높이는 데 도움이 되었다.
