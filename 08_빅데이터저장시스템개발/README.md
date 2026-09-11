# 빅데이터 저장시스템 개발 - NCS
- 빅데이터 저장모델 설계

---
## 전국 자동 복권 당첨 관련 저장 시스템 실습

| 파일명 | 설명 |
|---|---|
|`models.py`| SQLAIchemy 테이블 모델 정의 |
|`database.py`| DB 연결과 테이블 생성 |
|`loader.py`| CSV 적재 |
|`verify.py`| 검증. 대상 테이블을 정확히 조사 |
|`pipeline.py`| 통합 실행 |
|`README.md` | 실행 방법과 설계 설명 |

---

### pgAdmin에서 데이터베이스 준비
```sql
CREATE DATABASE lotteryaipdb;
```
---

### 입력 파일 준비

| 폴더 | 필요한 파일 |
| --- | --- |
| `CC:\Users\Administrator\bigdata2026\fastapi\09_빅데이터저장시스템개발\data`|`lottery_win.csv`|