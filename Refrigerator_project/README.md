# 냉장고 식재료 관리 시스템

FastAPI, PostgreSQL, Streamlit을 이용하여 냉장고 식재료와 유통기한을
관리하는 프로젝트입니다.

기존 애플리케이션을 Docker 컨테이너로 구성하고,
Docker Compose를 이용하여 FastAPI, PostgreSQL, Streamlit이
서로 통신하도록 구성하였습니다.


## 1. 주요 기능

- 식재료 등록
- 식재료 목록 조회
- 식재료 검색 및 필터링
- 식재료 수정
- 식재료 삭제
- CSV 파일을 이용한 식재료 일괄 등록
- 유통기한 임박 식재료 확인
- 유통기한 만료 식재료 확인 및 삭제
- 카테고리별 식재료 현황 시각화
- 보관방법별 식재료 현황 시각화
- 식재료 목록 페이지네이션


## 2. 사용 기술

| 구분 | 기술 |
|---|---|
| Backend | FastAPI |
| Frontend | Streamlit |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Validation | Pydantic |
| Container | Docker |
| Container Orchestration | Docker Compose |
| Data Processing | Pandas |


## 3. 프로젝트 구조

```text
Refrigerator_project_v5/
│
├── data/
│   └── upload.csv
│
├── frontend/
│   ├── Dockerfile
│   └── streamlit.py
│
├── routers/
│   └── ingredient.py
│
├── schema/
│   ├── request.py
│   └── response.py
│
├── main.py
├── database.py
├── models.py
├── requirements.txt
│
├── Dockerfile.api
├── docker-compose.yml
├── .env
├── .env.example
├── .gitignore
│
├── README.md
└── TROUBLESHOOTING.md
```


## 4. Docker 구성

프로젝트는 총 3개의 서비스로 구성하였습니다.

```text
사용자
  │
  │ localhost:8501
  ▼
┌─────────────────────┐
│ Streamlit           │
│ service: web        │
│ port: 8501          │
└──────────┬──────────┘
           │
           │ http://api:8000
           ▼
┌─────────────────────┐
│ FastAPI             │
│ service: api        │
│ port: 8000          │
└──────────┬──────────┘
           │
           │ db:5432
           ▼
┌─────────────────────┐
│ PostgreSQL          │
│ service: db         │
│ port: 5432          │
└──────────┬──────────┘
           │
           ▼
    postgres_data
       Volume
```

Docker Compose의 서비스 이름을 이용하여 컨테이너끼리 통신합니다.

| 출발 | 목적지 | 주소 |
|---|---|---|
| Streamlit | FastAPI | `http://api:8000` |
| FastAPI | PostgreSQL | `db:5432` |


## 5. 환경변수 설정

DB 접속정보와 API 주소를 코드에 직접 작성하지 않고 `.env`를 이용하여
관리합니다.

프로젝트 최상위에 `.env` 파일을 생성합니다.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=Food

DATABASE_URL=postgresql+psycopg2://postgres:1234@db:5432/Food
API_URL=http://api:8000
```

보안을 위해 `.env` 파일은 Git 저장소에 포함하지 않습니다.

`.gitignore`

```text
.env
```

실제 `.env` 대신 필요한 환경변수의 형식을 알려주기 위한
`.env.example`을 저장소에 포함할 수 있습니다.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your_password
POSTGRES_DB=Food

DATABASE_URL=postgresql+psycopg2://postgres:your_password@db:5432/Food
API_URL=http://api:8000
```


## 6. Docker 실행 방법

### 6-1. 프로젝트 다운로드

```bash
git clone <repository-url>
cd Refrigerator_project_v5
```

### 6-2. `.env` 설정

`.env.example`을 참고하여 프로젝트 최상위에 `.env` 파일을 생성합니다.

### 6-3. Docker 이미지 빌드 및 실행

```bash
docker compose up --build
```

위 명령 한 번으로 다음 서비스가 실행됩니다.

- PostgreSQL
- FastAPI
- Streamlit

### 6-4. 컨테이너 상태 확인

```bash
docker compose ps
```

정상적으로 실행되면 다음 3개의 컨테이너을 확인할 수 있습니다.

```text
fridge-db
fridge-api
fridge-web
```


## 7. 서비스 접속

### Streamlit

브라우저에서 다음 주소로 접속합니다.

```text
http://localhost:8501
```

### FastAPI Swagger

```text
http://localhost:8000/docs
```

### FastAPI 기본 API

```text
http://localhost:8000
```


## 8. 컨테이너 간 데이터 연동

식재료 등록 과정은 다음과 같습니다.

```text
Streamlit
    │
    │ POST /ingredients
    ▼
FastAPI
    │
    │ INSERT
    ▼
PostgreSQL
```

조회 과정은 반대 방향으로 진행됩니다.

```text
PostgreSQL
    │
    │ SELECT
    ▼
FastAPI
    │
    │ JSON Response
    ▼
Streamlit
```

Streamlit에서 식재료를 등록한 후 PostgreSQL 컨테이너에서
실제 데이터가 저장되었는지 확인할 수 있습니다.

```bash
docker compose exec db psql -U postgres -d Food
```

PostgreSQL 접속 후:

```sql
SELECT * FROM ingredients;
```

Streamlit에서 등록한 데이터가 조회되면
컨테이너 간 데이터 통신이 정상적으로 이루어진 것입니다.


## 9. 데이터 영속성

PostgreSQL 데이터가 컨테이너 삭제 후에도 유지될 수 있도록
Docker named volume을 사용하였습니다.

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

Docker Compose 최하단에는 다음 volume을 정의합니다.

```yaml
volumes:
  postgres_data:
```

일반적인 컨테이너 종료:

```bash
docker compose down
```

다시 실행:

```bash
docker compose up
```

기존 데이터가 유지되는지 확인할 수 있습니다.

주의:

```bash
docker compose down -v
```

명령은 volume까지 삭제하므로 DB 데이터 초기화가 필요한 경우에만
사용합니다.


## 10. Dockerfile 구성

### FastAPI

`Dockerfile.api`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Streamlit

`frontend/Dockerfile`

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY frontend/streamlit.py ./frontend/streamlit.py

EXPOSE 8501

CMD ["streamlit", "run", "frontend/streamlit.py", "--server.address=0.0.0.0", "--server.port=8501"]
```


## 11. Docker Compose

`docker-compose.yml`을 이용하여 3개의 서비스를 동시에 관리합니다.

```yaml
services:

  db:
    image: postgres:16
    container_name: fridge-db

    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}

    volumes:
      - postgres_data:/var/lib/postgresql/data

    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER} -d ${POSTGRES_DB}"]
      interval: 5s
      timeout: 5s
      retries: 10


  api:
    build:
      context: .
      dockerfile: Dockerfile.api

    container_name: fridge-api

    environment:
      DATABASE_URL: ${DATABASE_URL}

    ports:
      - "8000:8000"

    depends_on:
      db:
        condition: service_healthy


  web:
    build:
      context: .
      dockerfile: frontend/Dockerfile

    container_name: fridge-web

    environment:
      API_URL: ${API_URL}

    ports:
      - "8501:8501"

    depends_on:
      - api


volumes:
  postgres_data:
```


## 12. Docker 환경 대응

기존 로컬 실행환경에서도 프로젝트를 사용할 수 있도록
환경변수가 없는 경우 기본값을 사용하도록 구성했습니다.

### FastAPI → PostgreSQL

`database.py`

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/Food"
)
```

로컬 실행:

```text
localhost:5432
```

Docker 실행:

```text
db:5432
```

### Streamlit → FastAPI

`frontend/streamlit.py`

```python
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)
```

로컬 실행:

```text
http://127.0.0.1:8000
```

Docker 실행:

```text
http://api:8000
```


## 13. 프로젝트 종료

실행 중인 컨테이너를 종료하고 제거합니다.

```bash
docker compose down
```

PostgreSQL 데이터 volume은 유지됩니다.


## 14. 트러블슈팅

Docker 적용 과정에서 실제로 발생한 문제와 해결 과정은
`TROUBLESHOOTING.md`에 별도로 정리하였습니다.

주요 문제:

- Streamlit Dockerfile `CMD` 문법 오류
- Streamlit Dockerfile 이동에 따른 경로 오류
- `.env` 환경변수 인식 문제
- Docker 컨테이너 간 주소 설정
- PostgreSQL 데이터 영속성 구성


## 15. 프로젝트 결과

기존 FastAPI + PostgreSQL + Streamlit 기반 냉장고 식재료 관리
프로젝트를 Docker 환경으로 구성하였습니다.

Docker Compose를 이용하여 세 서비스를 한 번에 실행할 수 있도록
구성하였으며 다음과 같은 데이터 흐름을 구현하였습니다.

```text
Streamlit
    ↓
FastAPI
    ↓
PostgreSQL
```

또한 환경변수를 이용한 설정 분리와 PostgreSQL volume을 이용한
데이터 영속성을 적용하였습니다.