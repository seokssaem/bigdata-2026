# 학습일지 (daily-log.md)

## 작성자

* 이름: 장호균

---

## 2026-07-10

### 오늘 수업때 공부한 것들

```오전, 오후```

  - 시험 (의약품 연령금기 데이터 저장 프로젝트)
  - 프로젝트 구성
    ```
    drug_storage
    ┣ input
    ┃ ┗ KIDS_Age_Contraindications_final.csv
    ┣ __pycache__
    ┃ ┣ database.cpython-311.pyc
    ┃ ┣ loader.cpython-311.pyc
    ┃ ┣ models.cpython-311.pyc
    ┃ ┗ verify.cpython-311.pyc
    ┣ database.py
    ┣ dddd.ipynb
    ┣ loader.py
    ┣ models.py
    ┣ pipeline.py
    ┣ README.md
    ┗ verify.py
    ```
- models.py
  SQLAlchemy ORM을 이용하여 데이터베이스 테이블 구조를 정교하게 정의하였습니다.

  - 자동 증가 기본키(id) 배치
  - 필수 필수 필드 NOT NULL 제약조건 설정
  - 중복 방지용 복합 UNIQUE 제약조건 탑재

- database.py
PostgreSQL 데이터베이스와의 연결 세션을 세팅하고 관리합니다.

  - 프로그램 가동 시 테이블 방을 자동으로 개설해 주는 init_db() 내장
- loader.py
  대용량 파일을 5,000건씩 청크 단위로 쪼개어 읽어 메모리 과부하를 막습니다.

    - 중복 데이터 충돌 시 조용히 넘어가는 고속 업서트(ON CONFLICT DO NOTHING) 전략 적용
- verify.py
    - 데이터 적재가 완전히 완료된 후, 유실(NULL)이나 연령 도메인 범위 이탈 등의 이상치가 없는지 최종 품질 점검을 수행하는 무결성 검증 센터입니다.

- pipeline.py
   - 위의 모든 공정(구조 생성 / 고속 적재 / 교차 검증)을 총괄 지휘하여 원클릭으로 한 번에 가동해 주는 마스터 통합 파일입니다.



### 비고 (생각 및 집에서 할 일)

- fastapi학습
- 오늘 시험 친거 다시 한번 보기