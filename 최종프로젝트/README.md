# 생필품 가격 리포트

한국소비자원 **참가격** 공공데이터로 생필품 가격 변동을 추적하고, **다음 조사 가격을 예측**해서 보여주는 웹 서비스입니다.
데이터 수집·전처리부터 DB 저장, 웹 서비스, 로그인, Docker 배포까지 전 과정을 직접 구현했습니다.

- 과정: 코리아AI아카데미 빅데이터 분석 플랫폼 개발자 양성과정 최종 프로젝트
- 작성자: 김기완
- 배포 주소: http://43.202.81.175 (AWS Lightsail, 평가 기간 중 운영 후 삭제 예정)
- 문제 해결 기록: [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

---

## 1. 주제와 문제 정의

생필품 가격은 자주 바뀌지만, 한 상품의 가격이 **얼마나 올랐는지, 앞으로 오를지**를 한눈에 보기는 어렵습니다.
이 프로젝트는 다음 질문에 답하는 것을 목표로 합니다.

1. 이번 조사에서 가장 많이 오른(내린) 상품은 무엇인가?
2. 직전 조사 대비, 그리고 1년 전 같은 시기 대비 얼마나 변했는가? (% 와 원 단위 모두)
3. 다음 조사에서는 얼마가 될 것으로 예상되는가?
4. 관심 있는 상품을 내 계정에 모아 볼 수 있는가?

### 사용 데이터

| 항목 | 내용 |
|---|---|
| 출처 | 한국소비자원 참가격 (공공데이터) |
| 기간 | 2025-01-24 ~ 2026-08-28 |
| 규모 | 조사 38회, 약 417만 행 (매장별 개별 가격) |
| 전처리 후 | 상품 510개 (38회 중 30회 이상 조사된 상품만 사용) |

---

## 2. 주요 기능

| 기능 | 설명 |
|---|---|
| 메인 | 이번 조사 가격 상승 TOP 5, 최근 본 상품, 상품 검색·카테고리 필터, 페이지 이동(24개씩) |
| 상품 상세 | 현재가, 직전 대비, 전년 같은 시기 대비, 다음 조사 예상가 + 가격 추이 그래프 |
| 가격 랭킹 | 직전 대비 / 전년동기 대비 / 다음 예측, 상승·하락 전환 (상위 20개) |
| 회원 | 회원가입, 로그인, 로그아웃 |
| 즐겨찾기 | 로그인한 회원별로 DB에 저장 |
| 반응형 | 화면 폭이 좁으면 모바일 레이아웃으로 자동 전환 |
| JSON API | 상품·랭킹·예측 조회 API (Swagger 문서: `/docs`) |

---

## 3. 구성도

### 데이터 흐름

```mermaid
flowchart LR
    A[원본 CSV<br/>참가격 38회 조사] --> B[pandas<br/>병합·정제·카테고리]
    B --> C[pandas<br/>상품x조사일 평균<br/>등락률 계산]
    C --> D[scikit-learn<br/>선형회귀 예측]
    C --> E[(PostgreSQL<br/>6개 테이블)]
    D --> E
    E --> F[FastAPI<br/>라우터]
    F --> G[Jinja2 화면<br/>+ matplotlib 그래프]
    F --> H[JSON API]
```

### 배포 구조

```mermaid
flowchart LR
    U[사용자 브라우저] -->|http://서버IP :80| S
    subgraph S[AWS Lightsail - Ubuntu]
        direction LR
        API[api 컨테이너<br/>FastAPI 80 → 8000] --> DB[(db 컨테이너<br/>PostgreSQL 17<br/>볼륨에 영구 저장)]
    end
```

### ERD

```mermaid
erDiagram
    products ||--o{ price_history : "상품별 시계열"
    products ||--o{ price_changes : "상품별 등락률"
    products ||--o| predictions : "상품별 예측"
    users ||--o{ favorites : "회원별 즐겨찾기"
    products ||--o{ favorites : "즐겨찾기 대상"

    products {
        int id PK
        string product_name UK
        string category
    }
    price_history {
        int id PK
        int product_id FK
        date survey_date
        float avg_price
    }
    price_changes {
        int id PK
        int product_id FK
        date survey_date
        float avg_price
        float prev_price
        float price_diff
        float change_rate
        float yoy_price
        float yoy_diff
        float yoy_change_rate
    }
    predictions {
        int id PK
        int product_id FK, UK
        float base_price
        float predicted_price
        float expected_change_rate
        float raw_expected_change_rate
        datetime predicted_at
    }
    users {
        int id PK
        string username UK
        string password_hash
        datetime created_at
    }
    favorites {
        int id PK
        int user_id FK
        int product_id FK
        datetime created_at
    }
```

- `price_history`, `price_changes` 는 (상품, 조사일) 조합이 중복되지 않도록 UniqueConstraint 를 걸었습니다.
- `favorites` 는 (회원, 상품) 조합이 중복되지 않도록 UniqueConstraint 를 걸었습니다.
- `predictions` 는 상품당 최신 예측 1건만 유지합니다. `expected_change_rate` 는 ±15% 상한을 적용한 최종값, `raw_expected_change_rate` 는 보정 전 원본 예측값입니다.

---

## 4. 처리 과정과 설계 이유

| 단계 | 하는 일 | 이유 |
|---|---|---|
| 병합·정제 | 월별/격주별 CSV를 cp949 로 읽어 하나로 병합, 조사일 날짜형 변환, 중복 제거 | 원본이 여러 파일로 나뉘어 있고 인코딩이 cp949 |
| 조사 횟수 필터 | 38회 중 30회 이상 조사된 상품만 사용 → 510개 | 조사가 적은 신상품·조사 중단 상품은 추이가 의미 없음 |
| 카테고리 분류 | 직접 만든 정답표(`category_mapping.csv`)로 13개 공식 분류, 정답표에 없는 새 상품만 키워드 규칙으로 임시 분류 | 원본에 카테고리가 없고, 규칙만으로는 정확도가 낮았음 |
| 상품×조사일 평균 | 여러 매장 가격을 조사일마다 평균, 매장 수가 그 상품 중앙값의 30% 미만인 조사 시점은 제외(402건) | 표본이 갑자기 줄어든 시점의 평균은 노이즈 |
| 등락률 | 직전 조사 대비, 전년 같은 시기 대비(±20일 허용), % 와 원 단위 모두 계산 | 비율만으로는 체감하기 어려움 |
| 가격 예측 | 최근 10개 조사 시점으로 상품별 선형회귀, 예상 등락률을 ±15%로 제한 | 단순 모델이라 과도한 값 방지, 6개 미만 시점 상품은 제외 |
| 그래프 | 서버에서 matplotlib 으로 PNG 생성, 변동이 작은 상품(최저가 대비 30% 미만)은 Y축을 0부터 | 작은 변동이 크게 출렁여 보이는 착시 방지 |

---

## 5. 기술 스택

| 영역 | 사용 기술 |
|---|---|
| 데이터 처리·예측 | Python, pandas, scikit-learn |
| DB | PostgreSQL, SQLAlchemy (ORM) |
| 웹 | FastAPI, Jinja2 템플릿, HTML·CSS, JavaScript |
| 그래프 | matplotlib (서버에서 PNG 생성) |
| 인증 | 세션 쿠키(SessionMiddleware), PBKDF2-SHA256 비밀번호 해시 |
| 패키지 관리 | uv |
| 배포 | Docker, docker compose, AWS Lightsail (Ubuntu) |

---

## 6. 폴더 구조

```
price_report/
├── main.py                 # FastAPI 앱 진입점
├── database.py             # DB 연결 (DATABASE_URL)
├── models.py               # SQLAlchemy 모델 (6개 테이블)
├── security.py             # 비밀번호 해시, 로그인 세션 처리
├── templates_config.py     # Jinja2 설정
├── routers/                # 화면(pages, auth, charts)과 JSON API(products, prices, predictions, favorites)
├── schemas/                # API 응답 형식
├── services/               # 데이터 처리: preprocessing, categorize, aggregation, analysis, predictor, load_to_db
├── templates/              # Jinja2 HTML 템플릿
├── static/                 # CSS, JavaScript
├── data/                   # 원본 CSV(raw_csv/), 정답표(category_mapping.csv), 중간 결과
├── initdb/                 # export_db_sql.py 가 만드는 DB 초기 데이터(price_report.sql)
├── export_db_sql.py        # 내 DB의 가격 데이터를 SQL 파일로 내보내기
├── Dockerfile              # 앱 이미지
├── docker-compose.yml      # api + db 컨테이너 실행
├── requirements.txt        # Docker 이미지에 설치할 라이브러리
├── .env.example            # 환경변수 예시 (실제 .env 는 올리지 않음)
└── README.md
```

---

## 7. 실행 방법

### 7-1. 내 컴퓨터에서 실행 (개발용)

필요한 것: Python, [uv](https://docs.astral.sh/uv/), PostgreSQL (`price_report` 라는 DB 하나를 만들어 둠)

```bash
# 1) 라이브러리 설치
uv sync

# 2) 환경변수 파일 만들기 (.env.example 을 복사해서 값 채우기)
#    DATABASE_URL=postgresql://사용자:비밀번호@localhost:5432/price_report
#    SESSION_SECRET=아무_긴_문자열

# 3) 데이터 준비: data/raw_csv/ 에 원본 CSV 를 넣고 순서대로 실행
uv run python -m services.preprocessing   # 병합·정제 -> data/prices_combined.pkl
uv run python -m services.categorize      # 카테고리 분류
uv run python -m services.analysis        # 등락률 계산 -> data/analysis_result.pkl
uv run python -m services.predictor       # 가격 예측 -> data/price_predictions.csv

# 4) DB 에 적재 (회원 테이블 users/favorites 는 앱을 처음 실행할 때 자동 생성)
uv run python -m services.load_to_db

# 5) 서버 실행
uv run uvicorn main:app --reload
```

- 화면: http://localhost:8000
- API 문서(Swagger): http://localhost:8000/docs

### 7-2. Docker 로 실행 (배포와 같은 방식)

```bash
# 1) .env 만들기 (.env.example 참고)
#    POSTGRES_DB, POSTGRES_USER, POSTGRES_PASSWORD, SESSION_SECRET

# 2) 내 DB 의 가격 데이터를 SQL 파일로 내보내기 (initdb/price_report.sql 생성, 내 컴퓨터 DB 에 데이터가 적재돼 있어야 함)
uv run python export_db_sql.py

# 3) 실행
docker compose up -d --build
```

- 접속: http://localhost
- `initdb/price_report.sql` 은 **DB 컨테이너가 처음 만들어질 때 한 번만** 자동으로 실행됩니다.
  처음부터 다시 하려면 `docker compose down -v` 후 다시 `up` 합니다. (가입한 회원 정보도 함께 삭제됨)

---

## 8. 배포 (AWS Lightsail)

1. Lightsail 에서 Ubuntu 인스턴스 생성 (2GB 플랜), 고정 IP 연결, 방화벽에서 **80번 포트** 허용
2. 서버에 Docker 설치
   ```bash
   curl -fsSL https://get.docker.com | sudo sh
   sudo usermod -aG docker $USER   # 터미널을 다시 열어야 적용됨
   ```
3. 코드를 받고 서버용 `.env` 를 만든 뒤 실행
   ```bash
   git clone <저장소 주소>
   cd <저장소 폴더>
   nano .env                        # POSTGRES_*, SESSION_SECRET 입력 (비밀번호는 영문+숫자로 어렵게)
   docker compose up -d --build
   ```
4. 브라우저에서 `http://서버IP` 로 접속

### 배포 설계 포인트

- **컨테이너 2개**: 앱(api)과 DB(db)를 분리하고, db 가 healthcheck 를 통과한 뒤에 api 가 시작되도록 했습니다.
- **재시작 정책**: `restart: unless-stopped` 로 서버가 재부팅되어도 자동으로 다시 켜집니다.
- **데이터 영구 저장**: DB 데이터는 named volume 에 저장되어 컨테이너를 지워도 남습니다.
- **비밀 정보 분리**: DB 비밀번호와 세션 키는 `.env` 로 분리하고 GitHub 에는 올리지 않았습니다. (`.env.example` 만 제공)
- **초기 데이터**: 원본 CSV(수백 MB)를 서버에서 다시 계산하지 않고, 계산이 끝난 결과만 SQL 파일로 내보내 DB 최초 생성 시 자동으로 넣습니다.
- **한글 그래프**: slim 이미지에는 글꼴이 없어서 `fonts-nanum` 을 설치했습니다.

---

## 9. 보안

- 비밀번호는 **PBKDF2-SHA256**(반복 600,000회, 사용자마다 다른 salt)으로 해시해 저장하고 원문은 저장하지 않습니다.
- 로그인 상태는 서명된 세션 쿠키(14일, `same_site=lax`)로 유지합니다.
- 로그인 실패 시 아이디와 비밀번호 중 무엇이 틀렸는지 구분하지 않는 같은 메시지를 보여줍니다.
- 로그인 후 이동 주소(`next`)는 외부 사이트로 보내지 못하도록 검사합니다.
- `.env`(DB 비밀번호, 세션 키)는 저장소에 올리지 않습니다.

---

## 10. 결과 해석

- 최신 조사일(2026-08-28) 기준 직전 대비 상승 1위는 **크리넥스 클린케어 3겹(30롤)** 로 20,633원에서 32,816원(+59.0%)입니다.
  다만 이 상품은 조사 시점마다 평균가가 크게 출렁이는 상품이라(상세 그래프 참고), 큰 등락률이 곧 실제 가격 인상을 뜻하는 것은 아닐 수 있습니다.
  반대로 Dole 파인애플 슬라이스처럼 변동이 거의 없는 상품은 Y축을 0부터 그려서 평평하게 보이도록 했습니다.
- 다음 조사 예측 랭킹에는 예상 등락률이 상한(+15%)에 걸려 같은 값이 되는 상품이 많아서,
  같은 값끼리는 상한 적용 전 예측값이 큰 순서로 정렬합니다.

### 한계와 개선 방향

- 예측은 최근 10개 조사 시점의 **단순 선형회귀**라서 계절성, 행사, 외부 요인을 반영하지 못합니다. 실제 가격과 다를 수 있으며 화면에도 그 사실을 표시했습니다.
- 조사 매장과 매장 수가 조사마다 달라서 평균가가 달라 보일 수 있습니다. (표본이 크게 줄어든 시점은 제외했지만 완전한 보정은 아님)
- 계절성 등을 반영한 모델로 개선하고, 화면을 React 로 분리하는 것을 다음 단계로 생각하고 있습니다.
- 현재는 HTTP 로 서비스합니다. 실제 서비스라면 도메인과 HTTPS 인증서가 필요합니다.
- 새 CSV 를 추가해 같은 파이프라인을 다시 실행하면 새 데이터가 반영되도록 만들었습니다. 새 상품은 키워드 규칙으로 임시 분류되고, 검토 후 정답표에 추가합니다.

---

## 11. 출처

데이터 출처: 한국소비자원 참가격 (price.go.kr), 공공데이터포털
