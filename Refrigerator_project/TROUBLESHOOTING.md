
# TROUBLESHOOTING

본 문서는 냉장고 식재료 관리 프로젝트를 개발하고 Docker 환경으로
구성하는 과정에서 실제로 발생한 문제와 해결 과정을 기록한 문서입니다.

특정 팀원의 작업으로 구분하지 않고 프로젝트를 진행하면서 발생한 문제를
팀 공동으로 분석하고 해결한 내용을 정리하였습니다.

---

## Case 1. Streamlit Dockerfile의 CMD 구문 오류

### 1. 문제 상황

FastAPI, PostgreSQL, Streamlit을 Docker 환경에서 실행하기 위해

```bash
docker compose up --build
```

를 실행했으나 Streamlit 이미지 빌드 과정에서 다음 오류가 발생했습니다.

```text
dockerfile parse error on line 20:
unknown instruction: "streamlit",
```

### 2. 원인

`Dockerfile.streamlit`에서 Streamlit 실행 명령인 `CMD`를
다음과 같이 여러 줄로 작성한 것이 원인이었습니다.

```dockerfile
CMD [
    "streamlit",
    "run",
    "frontend/streamlit.py",
    "--server.address=0.0.0.0",
    "--server.port=8501"
]
```

Docker가 `"streamlit",` 부분을 새로운 Dockerfile 명령어로
해석하면서 `unknown instruction` 오류가 발생했습니다.

### 3. 해결

`CMD`를 한 줄의 JSON 배열 형식으로 수정했습니다.

```dockerfile
CMD ["streamlit", "run", "frontend/streamlit.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

FastAPI의 실행 명령도 동일한 형식으로 작성했습니다.

```dockerfile
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 4. 결과

Dockerfile 문법 오류가 해결되었고 Streamlit 이미지 빌드가
정상적으로 진행되었습니다.

---

## Case 2. Streamlit Dockerfile 이동 후 파일 경로 오류

### 1. 문제 상황

Streamlit과 관련된 Dockerfile을 프로젝트 최상위에서
`frontend` 폴더 안으로 이동했습니다.

```text
frontend/
├── Dockerfile
└── streamlit.py
```

이후 다시 빌드하는 과정에서 다음 오류가 발생했습니다.

```text
target web: failed to solve:
failed to read dockerfile:
open Dockerfile: no such file or directory
```

### 2. 원인

Dockerfile의 실제 위치를 변경했지만 `docker-compose.yml`의
Dockerfile 경로가 실제 위치와 일치하지 않았습니다.

또한 Streamlit Dockerfile에서는 프로젝트 최상위에 있는
`requirements.txt`가 필요하기 때문에 build context까지
`frontend` 폴더로 변경하면 루트의 파일에 접근할 수 없는 문제가 있었습니다.

### 3. 해결

build context는 프로젝트 최상위를 유지하고 Dockerfile의 위치만
`frontend/Dockerfile`로 지정했습니다.

```yaml
web:
  build:
    context: .
    dockerfile: frontend/Dockerfile
```

따라서 Streamlit Dockerfile에서도 다음 파일들을 정상적으로
복사할 수 있게 되었습니다.

```dockerfile
COPY requirements.txt .
COPY frontend/streamlit.py ./frontend/streamlit.py
```

### 4. 결과

Dockerfile을 `frontend` 폴더 안에 배치하면서도 프로젝트 최상위의
`requirements.txt`를 이용하여 정상적으로 이미지를 빌드할 수 있게
되었습니다.

---

## Case 3. Docker Compose에서 `.env` 환경변수를 읽지 못하는 문제

### 1. 문제 상황

DB 접속정보와 PostgreSQL 설정을 `docker-compose.yml`에 직접
작성하지 않고 `.env` 파일로 분리한 후 실행했을 때 다음 경고가
발생했습니다.

```text
The "POSTGRES_USER" variable is not set.
Defaulting to a blank string.

The "POSTGRES_PASSWORD" variable is not set.
Defaulting to a blank string.

The "POSTGRES_DB" variable is not set.
Defaulting to a blank string.
```

### 2. 원인

`docker-compose.yml`에서는 다음과 같이 환경변수를 참조하고 있었습니다.

```yaml
environment:
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  POSTGRES_DB: ${POSTGRES_DB}
```

하지만 Docker Compose가 `.env`에 정의된 값을 읽지 못하면서
환경변수가 빈 문자열로 처리되었습니다.

### 3. 해결

`.env`를 `docker-compose.yml`과 같은 프로젝트 최상위에 배치하고
`KEY=VALUE` 형식으로 환경변수를 정의했습니다.

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=1234
POSTGRES_DB=Food

DATABASE_URL=postgresql+psycopg2://postgres:1234@db:5432/Food
API_URL=http://api:8000
```

Docker Compose에서는 다음과 같이 사용했습니다.

```yaml
environment:
  POSTGRES_USER: ${POSTGRES_USER}
  POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
  POSTGRES_DB: ${POSTGRES_DB}
```

FastAPI와 Streamlit도 같은 방식으로 환경변수를 전달했습니다.

```yaml
api:
  environment:
    DATABASE_URL: ${DATABASE_URL}

web:
  environment:
    API_URL: ${API_URL}
```

설정값이 제대로 적용되는지는 다음 명령으로 확인했습니다.

```bash
docker compose config
```

또한 실제 접속정보가 Git 저장소에 올라가지 않도록 `.gitignore`에
다음 항목을 추가했습니다.

```text
.env
```

### 4. 결과

DB 접속정보와 API 주소를 코드 및 `docker-compose.yml`에서 분리하여
환경변수로 관리할 수 있게 되었습니다.

---

## Case 4. Docker 환경에서 `localhost`를 이용한 컨테이너 통신 문제

### 1. 문제 상황

기존 프로젝트는 로컬 환경에서 다음 주소를 사용하고 있었습니다.

```text
Streamlit → http://127.0.0.1:8000
FastAPI → localhost:5432
```

하지만 각 프로그램을 별도의 Docker 컨테이너로 분리하면
동일한 주소를 그대로 사용할 수 없었습니다.

### 2. 원인

Docker 컨테이너 내부에서 `localhost` 또는 `127.0.0.1`은
호스트 PC나 다른 컨테이너가 아니라 **현재 실행 중인 컨테이너 자신**을
의미합니다.

따라서 Streamlit 컨테이너에서 `127.0.0.1:8000`을 호출하면
FastAPI가 아니라 Streamlit 컨테이너 자신에게 접속하게 됩니다.

FastAPI의 `localhost:5432` 역시 PostgreSQL 컨테이너가 아니라
FastAPI 컨테이너 자신을 가리키게 됩니다.

### 3. 해결

Docker Compose의 서비스 이름을 컨테이너 간 주소로 사용했습니다.

```text
web → Streamlit
api → FastAPI
db  → PostgreSQL
```

따라서 컨테이너 간 연결 주소를 다음과 같이 구성했습니다.

```text
Streamlit → http://api:8000
FastAPI → db:5432
```

기존 로컬 실행 환경도 사용할 수 있도록 Python 코드에서는
환경변수와 기본값을 함께 사용했습니다.

`database.py`

```python
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://postgres:1234@localhost:5432/Food"
)
```

`frontend/streamlit.py`

```python
API_URL = os.getenv(
    "API_URL",
    "http://127.0.0.1:8000"
)
```

### 4. 결과

로컬에서 직접 실행할 때는 기존 `localhost` 주소를 사용하고,
Docker Compose에서는 `api`, `db` 서비스 이름을 사용하도록
실행환경을 분리할 수 있게 되었습니다.

최종적인 컨테이너 통신 구조는 다음과 같습니다.

```text
Streamlit
    ↓
http://api:8000
    ↓
FastAPI
    ↓
db:5432
    ↓
PostgreSQL
```

---

## Case 5. PostgreSQL 컨테이너 재생성 시 데이터 유지 문제

### 1. 문제 상황

Docker 컨테이너는 삭제 후 다시 생성할 수 있기 때문에
PostgreSQL 컨테이너를 삭제했을 때 기존 식재료 데이터까지
사라질 가능성이 있었습니다.

### 2. 원인

PostgreSQL의 데이터를 컨테이너 내부에만 저장하면 컨테이너가
삭제될 때 데이터도 함께 영향을 받을 수 있습니다.

### 3. 해결

`docker-compose.yml`에 PostgreSQL named volume을 추가했습니다.

```yaml
db:
  volumes:
    - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

컨테이너를 종료할 때는 다음 명령을 사용했습니다.

```bash
docker compose down
```

그리고 다시 실행했습니다.

```bash
docker compose up
```

### 4. 결과

컨테이너의 실행 상태와 PostgreSQL 데이터 저장 영역을 분리할 수
있게 되었고, 컨테이너를 다시 생성해도 기존 데이터를 유지할 수 있는
구조로 개선했습니다.

---

# 최종 정리

이번 프로젝트에서는 FastAPI, PostgreSQL, Streamlit을 각각
Docker 환경에서 실행하고 `docker-compose.yml`을 이용하여 하나의
서비스로 연결했습니다.

프로젝트 진행 과정에서 Dockerfile 실행 명령 오류, Dockerfile 경로
문제, `.env` 환경변수 설정 문제, 컨테이너 간 네트워크 주소 문제,
데이터 영속성 문제 등을 확인하고 해결했습니다.

최종 구성은 다음과 같습니다.

```text
사용자
  ↓
Streamlit 컨테이너
  ↓
FastAPI 컨테이너
  ↓
PostgreSQL 컨테이너
  ↓
Docker Volume
```

이를 통해 단순히 각각의 프로그램을 컨테이너화하는 것뿐만 아니라
컨테이너 간 통신, 환경변수 관리, 데이터 영속성까지 함께 고려하여
프로젝트를 구성할 수 있었습니다.