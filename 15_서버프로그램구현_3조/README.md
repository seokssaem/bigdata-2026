# 2026 FIFA 월드컵 데이터 API

**사용 데이터셋:** 2026 FIFA 월드컵(북중미) 선수·경기·팀 기록(players/matches/teams, 총 3개 테이블).
**선정 사유:** 팀에서 직접 전처리(인코딩 정리, 한국어 변환, KST 시간대 변환)까지 마친 정제 데이터가 있어 그대로 활용.

PostgreSQL에 저장된 데이터를 FastAPI로 조회·수정하는 실습 프로젝트입니다. (Todo/User 실습 때 배운 구조를 그대로 재사용했습니다)

---

## 1. 프로젝트 구조

```
worldcup-api/
├── main.py                # FastAPI 앱 진입점
├── database/
│   ├── db_connection.py    # DB 엔진 + SessionFactory
│   └── orm.py               # Base 클래스
├── models.py                # SQLAlchemy ORM 모델 (Player/Match/Team)
├── schema/
│   ├── request.py           # 요청 Pydantic 모델
│   └── response.py          # 응답 Pydantic 모델
├── auth/
│   └── jwt.py                # JWT 발급/검증 (PyJWT)
├── routers/
│   ├── users.py              # 로그인
│   ├── players.py            # 선수 CRUD
│   ├── matches.py            # 경기 조회
│   ├── teams.py               # 팀 조회
│   └── stats.py                # pandas 통계
├── streamlit_api/              # streamlit 모델(하위 항목에서 추가 설명)
├── data/                       # players.csv, matches.csv, teams.csv
├── schema.sql                  # 테이블 정의 (한국어 컬럼 코멘트 포함, 전체 컬럼 버전)
├── setup_database.py           # schema.sql 실행 + CSV 적재
└── .env                        # 환경설정 값
```

## 2. 서버 실행
```bash
uvicorn main:app --reload
```
브라우저에서 http://127.0.0.1:8000/docs 접속 → Swagger UI에서 바로 테스트 가능.

쓰기(POST/PUT/DELETE) API는 로그인이 필요합니다. `/docs` 우측 상단 **Authorize** 버튼 클릭 →
`username: admin`, `password: admin1234` (`.env`에서 변경 가능)로 로그인하면 이후 요청에 토큰이 자동으로 붙습니다.

```bash
streamlit run app.py
```
Streamlit 서버 실행

---

## 3. 엔드포인트

| Method | URL | 설명 | 로그인 |
|---|---|---|---|
| POST | `/users/login` | 로그인, JWT 토큰 발급 | - |
| GET | `/players` | 선수 목록 (team/position/search 필터, 정렬, 페이지네이션) | - |
| GET | `/players/{id}` | 선수 상세 | - |
| POST | `/players` | 선수 추가 | ✅ |
| PUT | `/players/{id}` | 선수 정보 수정 (일부 필드만 전송 가능) | ✅ |
| DELETE | `/players/{id}` | 선수 삭제 | ✅ |
| GET | `/matches` | 경기 목록 (team/round 필터) | - |
| GET | `/matches/{id}` | 경기 상세 | - |
| GET | `/teams` | 팀 목록 (이름 검색) | - |
| GET | `/teams/{id}` | 팀 상세 | - |
| GET | `/stats/top-scorers` | pandas로 계산한 90분당 득점 상위 선수 | - |
| GET | `/stats/team-goal-diff` | pandas로 집계한 팀별 득실차/승점 순위표 | - |

## 4. 시도해본 것들

- 필터링/검색/정렬/페이지네이션 (`/players`, `/matches`)
- pandas로 SQL 결과 후처리 통계 API (`/stats/*`)
- JWT 로그인 붙여서 쓰기 API 보호 (PyJWT, jwt_create.py/jwt_checked.py 실습 확장)
- 컬럼이 250개 넘는 테이블 중 핵심 컬럼만 ORM으로 매핑하고, 나머지는 pandas로 직접 접근
- 컬럼 화이트리스트로 `sort_by` SQL 인젝션 방지
- PUT에서 일부 필드만 보내도 되도록 Optional 처리 (`exclude_unset=True`)

## 5. 트러블슈팅(삽질)

---

### 1. (데이터 정제 단계) 엑셀에서 `score`(`2-0`), `formation`(`4-3-3`) 값이 날짜로 자동 변환됨

- **시도**: 위와 같이 엑셀로 CSV 확인
- **문제점**: `1-0`, `4-3-3` 같은 하이픈 포함 숫자 문자열을 엑셀이 날짜로 자동 인식해서 `2001-01-00` 같은 이상한 값으로 표시됨. (PostgreSQL 적재 자체에는 영향 없음 — 어디까지나 엑셀에서 보기용 문제)
- **해결방안**: 엑셀용 CSV에서만 해당 컬럼 값을 `="2-0"` 형태(엑셀 수식으로 강제 텍스트 취급)로 감싸서 저장

---

### 2. PUT 수정 API에서 계속 422 발생

- **시도**: `PUT /players/{id}`에 선수의 `goals` 값 하나만 바꾸려고 `{"goals": 10}` 전송
- **문제점**: `422 Unprocessable Entity`. Pydantic 모델(`PlayerCreate`)을 그대로 수정용으로 재사용했더니 필수 필드가 빠졌다고 오류가 발생함.
- **해결방안**: 생성용(`PlayerCreate`)과 수정용(`PlayerUpdate`) 스키마를 분리하고, 수정용은 전 필드를 `Optional`로 선언. 라우터에서도 `payload.model_dump(exclude_unset=True)`로 **실제로 보낸 필드만** 골라서 업데이트하도록 변경 → 해결

- 문제점을 파악하는데에 오랜시간이 걸린 부분.
- 예를들어 { "player": "손흥민", "team": "대한민국", "goals": 5, "assists": 3 } 과 같은 DB에서 `goals`만 수정을 하고싶다고 할때
- PUT항목에서 { "goals": 10 } 과 같이 요청을 보낸다.
- 코드 내에서 `model_dump()`를 그냥 쓰게되면 {"player": None, "team": None, "goals": 10.0, "assists": None} 과 같이 다른 필수 컬럼에 **None**이 채워짐.
- 이로인해서 기존에 있던 정보까지 지워지는 대참사가 발생하게된다.
- 따라서 `payload.model_dump(exclude_unset=True)`를 작성하여 내가 수정하고싶은 필드만 수정하게끔 하였다.

---

### 3. SQLAlchemy 모델을 손으로 쓰다가 포기

- **시도**: `players`(72개), `teams`(136개) 테이블 컬럼을 하나하나 선언
- **문제점**: 컬럼 250개 넘게 손으로 타이핑하다가 오타/누락이 계속 발생, 컬럼명 하나 바뀌면 모델도 같이 고쳐야 하는 이중 관리 문제
- **해결방안**: 처음엔 `sqlalchemy.ext.automap`으로 전체를 자동 리플렉션했는데, 응답 JSON에 안 쓰는 컬럼까지 다 나와서 오히려 이해하기 어려웠음. 최종적으로는 실습 때 배운 `Mapped`/`mapped_column` 방식 그대로, **API에서 실제로 쓰는 핵심 컬럼만** 모델에 매핑하고, 나머지 세부 컬럼은 `/stats` 라우터처럼 `pandas.read_sql()`로 필요할 때만 직접 읽어오는 방식으로 정리

---

### 4. `went_to_penalties` 같은 boolean 컬럼에 문자열 `"true"/"false"`를 그대로 넣어도 되는가?

- **시도**: CSV에는 `true`/`false` 문자열로 저장돼 있는데, 이걸 그대로 `pandas.to_sql()`로 BOOLEAN 컬럼에 적재
- **문제점**: PostgreSQL이 문자열 `'true'`/`'false'`를 boolean으로 해줄지 확신이 없었음.
- **해결방안**: PostgreSQL은 `'true'`/`'false'` 텍스트를 boolean으로 암묵적으로 해주기 때문에 문제없이 적재됨을 확인.

---

### 5. 정렬 파라미터(`sort_by`)를 문자열 그대로 `order_by()`에 넣으려고 시도

- **시도**: 쿼리 파라미터로 받은 `sort_by` 값을 바로 `getattr(Player, sort_by)`에 넣어서 사용
- **문제점**: 사용자가 아무 문자열이나(`players_id`, 심지어 존재하지 않는 컬럼명) 넘기면 오류가 나서 코드가 종료가 되거나, 조회되지 않아야할 정보까지 조회되는 경우가 발생함.
- **해결방안**: 정렬 가능한 컬럼을 (`SORTABLE_COLUMNS`)로 미리 제한해두고, 화이트리스트에 없는 값이 오면 400 에러를 명시적으로 반환하도록 처리

---

### 6. Streamlit을 실행 시켰을 때 404에러가 뜸

- **시도**: uvicorn실행 후 streamlit 실행
- **문제점**: FastAPI에 연결할 수 없다고 뜸. `404 Not Found` 발생
- **해결방안**: Streamlit에서 헬스체크하려고 요청을 하였으나 `/health`엔드 포인트가 존재하지않아 오류가 발생. `main.py`에 `@app.get("/health")` 문구 작성

---

### 7. load_csv에서 UTF-8 인코딩 실패
- **시도**:setup_database.py파일을 python으로 실행
- **문제점**: csv파일 하나가 UTF-8 형태가 아니라 인코딩 실패
- **해결방안**: UTF-8형태로 우선 인코딩 하고 인코딩 실패한 csv파일은 CP949로 재시도하는 코드 작성

---

### 8. `players`, `playersE` 두 개 테이블 중복 생성
- **시도**: setup_database.py파일을 python으로 실행
- **문제점**: playerse와 playersE 테이블 두개 생성
- **해결방안**: 테이블명을 `playerse`(소문자)로 통일

---

### 9. `setup_database.py` 재실행 시
- **시도**: Streamlit에서 한국어 이름으로 선수 검색
- **문제점**: 선수 이름을 영어에서 한국어로 표기하는 과정에서 사람마다 표기법이 달라(예: "손흥민"을 영어 발음대로 다르게 표기하는 경우 등), 사용자가 알고 있는 영어 이름으로는 검색이 되지 않는 경우 발생
- **해결방안**: 영어 이름이 담긴 `playerse` CSV를 별도 테이블로 추가하고, `players_id`(PK)로 두 테이블을 매칭. SQLAlchemy의 `or_`를 사용해 한글 이름 또는 영어 이름 중 하나라도 일치하면 검색되도록 수정하고, `ilike`로 대소문자 구분 없는 부분 검색도 가능하도록 개선

---

### 10. 한국어로만 선수 검색 시, 사람마다 다른 영어 표기법 때문에 조회 안 되는 문제
- **시도**: streamlit에서 한국어로 선수 검색
- **문제점**: 영어를 한국어로 변경했기 때문에 사람마다 표기법이 달라 검색이 안 되는 경우 발생
- **해결방안**: 영어로 된 csv파일을 추가하고 or_ 코드를 통해 영어로 검색해도 선수가 검색되도록 수정 가능, ilike 코드를 통해 부분적인 검색도 가능하도록 수정

---

## 6. 스트림릿 구조 및 설명

`Streamlit_api` 폴더는 FastAPI에서 제공하는 월드컵 API를 사용하여
사용자가 선수, 국가, 경기 및 통계 정보를 쉽게 조회할 수 있도록 만든 streamlit 웹 애플리케이션입니다.

전체적인 데이터 흐름은 다음과 같습니다.

PostgreSQL -> FastAPI -> Streamlit -> 사용자 화면

Streamlit에서 직접 PostgreSQL을 조회하는 것이 아니라 `api_client.py`을 통해 FastAPI 엔드포인트를 호출하고 전달받은 
Json 데이터를 화면에 출력합니다.


### 1. 폴더 구조
```
streamlit_api
 ┣ data
 ┃ ┗ matches.csv
 ┣ pages
   ┣ home.py
   ┣ home.zip
   ┣ matches.py
   ┣ player_detail.py
   ┣ player_search.py
   ┣ stats.py
   ┗ teams.py
```
----

`app.py` : streamlit 애플리케이션의 시작 파일이며 각 페이지로 이동할 수 있는 메뉴를 구성합니다.

`api_client.py` : FastAPI 서버에 ATTP 요청을 보내고 선수, 경기, 국가, 통계 데이터를 받아오는 역할

`pages/home.py` : 프로젝트 소개 및 주요 기능을 보여주는 메인 화면 입니다

`pages/player_search.py` : 선수 이름, 국가, 포지션 등의 조건으로 선수를 검색하고 정렬할 수 있는 화면입니다.

`pages/player_detail.py` : 선택한 선수의 국가, 포지션, 나이, 소속 클럽, 경기 수, 득점, 도움 등의 상세 정보를 보여줍니다.

`pages/matches.py` : 월드컵 경기 목록 및 경기 정보를 조회하는 화면입니다.

`pages/teams.py` : 참가 국가를 검색하고 국가별 정보를 조회하는 화면입니다.

`pages/stats.py` : 훨드컵 최종 순위와 선수 득점 관련 통계를 표와 그래프로 시각화 하는 화면입니다.

---
### 2. 주요기능

- 선수 이름 검색
- 국가별 선수 검색
- 포지션별 선수 검색
- 선수 목록 정렬
- 선수 상세 정보 조회
- 월드컵 경기 조회
- 참가 국가 조회
- 월드컵 최종 순위 확인
- 선수 득점 통계 조회 및 시각화

---

### 3.구현목적
FastAPI의 API 기능을 Swagger에서만 확인하는 것에 그치지 않고,\
Streamlit을 이용해 실제 사용자가 월드컵 데이터를 검색하고 확인할 수 있는 웹 화면을 구현했습니다.



## 7. 팀원별 작업 내용

| 팀원 | 담당 |
|---|---|
| 김수완 | api 코드 작성|
| 장호균 | streamlit 코드 작성|
| 태두혁 | ppt제작 및 api 기능 추가|
| 공동작업| 주제선정, 전체적인 코드 검토 및 오류 수정|
