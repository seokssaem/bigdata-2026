# Docker 트러블슈팅

FastAPI, Streamlit, PostgreSQL을 Docker로 컨테이너화하고 `docker-compose`로
연동하는 과정에서 실제로 부딪힌 문제와 해결 과정을 정리한다.

---

## 실행 방법
```bash
# 경로에 한글이 포함되어 있을 경우, docker-compose up --build --> gRPC 에러 발생. 아래 명령어를 사용할 것!
# 경로에 한글이 포함되지 않았다면 상관 없음.
docker-compose build fastapi
docker-compose build streamlit
docker-compose up   
```
---

## 문제 1 — gRPC 오류로 이미지 빌드 에러

**증상**: `docker-compose up --build` 실행 시 이미지 빌드 단계에서 아래 에러가 발생하며 빌드가 중단됨.

```
failed to dial gRPC: rpc error: code = Internal desc = rpc error: code = Internal desc = header key "x-docker-expose-session-sharedkey" contains value with non-printable ASCII characters
```

이미지 하나(`postgres:16`)는 정상적으로 pull되었지만, 직접 빌드해야 하는 `fastapi`, `streamlit` 이미지 빌드 단계에서만 매번 이 오류가 반복됐다.

**원인**: 프로젝트 폴더 경로에 한글이 포함되어 있었다.

```
...\TEST\16_통합구현_김동욱\16_통합구현_1조\
```

Docker의 빌드 엔진(BuildKit)은 클라이언트와 세션을 열 때 경로 관련 정보를 HTTP 헤더에 실어 전달하는데, HTTP 헤더 규격상 ASCII 문자만 허용된다.
경로에 `통합구현`처럼 한글(non-ASCII)이 포함되어 있으면 이 헤더 값이 깨지면서 세션 자체를 열지 못해 위와 같은 gRPC 오류로 이어졌다.

**해결**: 프로젝트 폴더를 한글이 전혀 없는 경로로 이동시켰다.

```
변경 전: ...\TEST\16_통합구현_김동욱\16_통합구현_1조\
변경 후: ...\TEST\16_TEST\
```

폴더 이름뿐 아니라 상위 경로 전체에 한글이 하나도 없어야 하며, 옮긴 뒤 다시 `docker-compose up --build`를 실행하니 정상적으로 이미지가 빌드됐다.

**포인트**: Docker Desktop for Windows 환경에서는 프로젝트 경로에 한글(또는 비ASCII 문자)이 섞여 있으면 컨테이너 실행 이전에,
BuildKit과의 통신 단계에서부터 막힐 수 있다는 것을 알게 됐다. 에러 메시지만 보면 코드나 설정 파일 문제처럼 보이지만, 실제 원인은 파일 시스템 경로에 있었다.
Docker 프로젝트는 가급적 영문/숫자로만 이루어진 짧은 경로에 두는 것이 안전하다는 것을 알게 되었다.

---

## 문제 2 — FastAPI 컨테이너가 DB 컨테이너보다 먼저 접속을 시도해 서버가 죽음

**증상**: 경로 문제를 해결한 뒤 `docker-compose up --build`를 다시 실행하니 이미지 빌드는 성공했지만,
`movie_fastapi` 컨테이너가 시작되자마자 아래 에러를 내며 종료됐다.

```
psycopg2.OperationalError: connection to server at "db" (172.18.0.2), port 5432 failed: Connection refused
...
ERROR:    Application startup failed. Exiting.
```

같은 시각 `movie_db` 로그에는 `"database cluster will be initialized"`, `"creating subdirectories"` 등 PostgreSQL이 아직 최초 초기화(initdb) 작업을 진행 중이라는 로그가 찍히고 있었다.

**원인**: `docker-compose.yml`에서 `fastapi` 서비스에 `depends_on: - db`만 지정해 두었는데, `depends_on`은 "db 컨테이너가 시작되었는지"만 보장할 뿐
"PostgreSQL이 실제로 접속을 받을 수 있는 상태인지"까지는 보장하지 않는다. DB 컨테이너는 최초 실행 시 initdb 작업(디렉토리 생성, 설정 파일 생성 등)에
시간이 걸리는데, 그 사이 5432 포트는 아직 열리지 않은 상태다. 그런데 `main.py`의 `lifespan` 함수는 앱이 뜨자마자 `Base.metadata.create_all(bind=engine)`을
바로 실행하도록 되어 있어서, DB가 준비되기 전에 접속을 시도하다 실패했고, 그 예외가 그대로 앱 시작 실패로 이어져 FastAPI 컨테이너 자체가 종료됐다.

**해결**: `docker-compose.yml`의 `db` 서비스에 `healthcheck`를 추가하고, `fastapi` 서비스가 `db`의 헬스체크 통과(healthy)를 실제로 기다리도록 `depends_on` 조건을 수정했다.

```yaml
db:
  image: postgres:16
  healthcheck:
    test: ["CMD-SHELL", "pg_isready -U postgres -d moviedb1"]
    interval: 5s
    timeout: 5s
    retries: 10

fastapi:
  depends_on:
    db:
      condition: service_healthy
```

수정 후 다시 실행하니 로그에 `Container movie_db Healthy`가 찍힌 뒤에야 `movie_fastapi`가 시작되었고, `CREATE TABLE movie`, `CREATE TABLE actor` 등이
에러 없이 실행되어 `Application startup complete.`로 정상 기동됐다.

**포인트**: `depends_on`은 컨테이너의 "시작 순서"만 정할 뿐 "서비스가 실제로 쓸 준비가 됐는지"는 확인해 주지 않는다는 것을 확인했다.
특히 PostgreSQL처럼 최초 실행 시 초기화 시간이 필요한 서비스는, 단순 순서 지정이 아니라 `healthcheck` + `condition: service_healthy` 조합으로
"진짜 준비 완료"를 기다리게 만들어야 한다는 걸 알게 됐다.

---

## 문제 3 — 한글 경로 문제를 추가로 분석
 
**증상**: 문제 1에서 폴더를 영문 경로로 옮겨 문제를 해결했지만, 한글이 포함된 경로로 정상 작동시킬 방법이 있는지 추가로 검증해보았다.
먼저 원래 한글 경로로 프로젝트를 복사해 두고, 그 안에서 여러 명령을 하나씩 시도하며 어느 지점에서 정확히 실패하는지 좁혀나갔다.

**전개**: 우선 4가지 방법을 생각했다.

1. Legacy 빌더로 전환 (DOCKER_BUILDKIT=0)
BuildKit 자체를 안 쓰면 문제 지점을 우회할 수 있지 않을까 하는 가설. 다만 실제로 검증하지는 못했고, Legacy builder 전환을 검토했으나,
해당 방식이 현재 deprecated 상태이며 향후 제거 예정이라는 것을 알게되어 향후 Docker 버전과의 호환성이 보장되지 않아 장기적인 해결책으로 부적절하다고 판단함.

2. WSL2 내부로 프로젝트 이동
Windows 경로 대신 리눅스 파일시스템 경로를 쓰면 애초에 인코딩 문제를 피할 수 있다는 가설. 프로젝트 실제 저장 위치 자체가 바뀌어야 해서 시도하지 않았다.

3. 디렉토리 정션(mklink /J)으로 영문 별칭 경로 만들기
한글 폴더는 그대로 두고, C:\docker-work 같은 영문 별칭을 만들어 Docker에는 그 경로만 보여주는 방법.
정션은 해당 컴퓨터에만 적용되는 파일시스템 설정이라 프로젝트를 압축해서 다른 사람에게 준다면 정션 정보가 같이 넘어가지 않는다는 한계가 있어, 제출용 프로젝트에는 맞지 않는다고 판단하고 기각했다.

4. 이미지를 미리 빌드해서 docker-compose.yml을 build: 대신 image:로 구성
빌드 자체를 compose 밖에서 미리 끝내면 문제를 우회할 수 있지 않을까 하는 가설이다.
    1. 우선 테스트를 위해 컴포즈를 제외하고 fastapi만 빌드해보았다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker build -t movie-fastapi:latest -f Dockerfile.fastapi .
        ```
        그 결과 한글 경로를 포함하고 있음에도 불구하고 정상적으로 빌드가 진행되었다.

    2. 혹시나 하는 생각에 컴포즈를 거치면서 fastapi를 빌드해보았다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker-compose build fastapi
        ```
        문제없이 빌드를 성공했다.

    3. 이어서 컴포즈를 거치면서 streamlit을 빌드해보았다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker-compose build streamlit
        ```
        이 결과도 역시 문제없이 빌드를 성공했다.

    4. 이미 빌드된 fastapi와 streamlit가 정상동작하는지 확인했다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker-compose up --no-build
        ```
        깔끔하게 실행되었다.

    5. 다시 빌드를 시도해보았다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker-compose build
        ```
        이번 테스트에서는 gRPC 에러가 다시 발생하였다.

    6. 마지막 테스트로 no-build 명령어 없이 실행해보았다.
        ```bash
        # TEST/16_통합구현_김동욱/16_통합구현_1조/
        docker-compose up
        ```
        정상적으로 실행되었다.

**결론**: 개별로 하나씩 빌드하면 한글 경로가 포함되어도 괜찮지만, 여러 개를 한 번에 빌드하면 실패한다는 것을 알게되었다.

## 문제 4 - 경로에 한글이 포함되었을 때, 여러 개를 한 번에 빌드하면 gRPC 에러가 발생한다.

**증상**:
```
docker-compose build time="2026-09-07T14:18:49+09:00" level=warning msg="C:\\Users\\Administrator\\bigdata2026\\bigdata2026-basic\\TEST\\16_통합구현_김동욱\\16_통합구현_1조\\docker-compose.yml: the attribute version is obsolete, it will be ignored, please remove it to avoid potential confusion" #1 [internal] load local bake definitions #1 reading from stdin 1.29kB 0.0s done #1 DONE 0.0s [+] build 0/2 - Image 16__1-fastapi Building 0.5s - Image 16__1-streamlit Building 0.5sfailed to dial gRPC: rpc error: code = Internal desc = rpc error: code = Internal desc = header key "x-docker-expose-session-sharedkey" contains value with non-printable ASCII characters
``` 


**전개**: 출력에 `load local bake definitions` 가 포함된 것을 보고 bake를 비활성화하고 시도하기로 했다.
```bash
# TEST/16_통합구현_김동욱/16_통합구현_1조/
COMPOSE_BAKE=false docker-compose build
```
실패였다. bake의 비활성화가 제대로 작동하지 않았다.
찾아보니 Docker Compose v5 이상에서는 bake가 강제되고 비활성화하는 것이 불가능하다는 것을 알게 되었다.

**결론**: 한글 폴더 구조를 유지하기 위해서는 빌드를 따로 해야한다.
빌드를 따로하고 난 후에는 `docker-compose up` 명령어로 한 번에 실행이 가능하다.