# NCS 빅데이터 처리 시스템 실습

## Steam 게임 데이터 처리시스템
저장시스템 실습(steam_games)에서 만든 PostgreSQL 테이블을 이용하여 배치 처리, 이벤트 처리 모듈을 실행하는 예제

### 1. 전제 조건
저장시스템(steam_games) 실습이 완료되어 있어야 한다.

| DB | 테이블 |
| --- | --- |
| `gamesdb` | `games` |
| `gamesdb` | `game_genres` |

### 2. 필요한 라이브러리
```bash
pip install sqlalchemy "psycopg[binary]"
```

### 3. 환경변수
기본값은 저장시스템 실습과 같은 DB(`gamesdb`), 같은 비밀번호(`1234`)

```bash
set DATABASE_URL=postgresql+psycopg://postgres:1234@localhost:5432/gamesdb
```

### 4. 실행

```bash
python pipeline.py
```

### 5. 결과 테이블

| DB | 결과 테이블 | 설명 |
| --- | --- | --- |
| `gamesdb` | `batch_genre_summary` | 배치 처리 결과. 장르별 게임 수 / 평균 가격 / 평균 메타크리틱 점수 등 |
| `gamesdb` | `event_game_alerts` | 이벤트 처리 결과. metacritic_score > 85 인 고평가 게임 알림 |

### 6. 확인 SQL

```sql
-- 입력 테이블
SELECT COUNT(*) FROM games;
SELECT COUNT(*) FROM game_genres;
SELECT COUNT(DISTINCT genre_name) FROM game_genres;   -- batch_genre_summary 행수와 비교

-- 배치 처리 결과
SELECT * FROM batch_genre_summary ORDER BY game_count DESC;

-- 이벤트 처리 결과
SELECT * FROM event_game_alerts ORDER BY metric_value DESC LIMIT 20;

-- 이벤트 결과를 원본에서 같은 조건으로 재계산해서 교차검증
SELECT COUNT(*) FROM games WHERE metacritic_score > 85;
```

### 7. 실습 목표
- 저장시스템은 데이터를 안전하게 저장하는 것이 목표
- 처리시스템은 저장된 데이터를 목적에 맞게 가공하여 새로운 결과를 만드는 것이 목표

- Spark / Kafka 설치 없이 Python과 PostgreSQL로 처리 로직을 먼저 구현해서 이해
- 같은 로직을 Spark SQL, Kafka, Flink, Esper, Hadoop, Hive 등 같은 도구로 확장할 수 있다.
