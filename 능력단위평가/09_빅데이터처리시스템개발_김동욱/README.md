# 빅데이터 처리시스템 개발

## PostgreSQL에 저장된 테이블 설명

### water 정보 (전체 84행)

| 컬럼명 | 자료형 | 설명 |
| --- | --- | --- |
| `water_id` | Integer | 대리키 |
| `정수장` | String(10) | 정수장명 |
| `구분` | String(10) | 정수장 구분 |
| `ph` | Numeric(5,2) | pH농도 |
| `탁도` | Numeric(5,2) | 탁도 |
| `잔류염소` | Numeric(5,2) | 잔류염소 |
| `검사시기` | Date | 검사 연-월-일(일은 1로 고정) |

UNIQUE 제약 : `정수장 + 구분 + 검사시기` (`uq_water_key`)

---
### area 정보 (전체 155행)
| 컬럼명 | 자료형 | 설명 |
| --- | --- | --- |
| `area_id` | Integer | 대리키 |
| `정수장` | String(10) | 정수장명 |
| `구군` | String(10) | 구/군 이름 |
| `행정구역` | String(10) | 행정동 이름 |
| `급수분류` | String(10) | 전지역 / 일부지역 |

UNIQUE 제약 : `정수장 + 구군 + 행정구역 + 급수분류` (`uq_area_key`)

---
### 테이블 관계
![ERD](./08_ERD.png)

water 테이블의 정수장 컬럼과 area 테이블의 정수장 컬럼이 같다.

area 테이블에서 행정구역마다 어느 정수장에서 물이 공급되는지 확인할 수 있고,  
water 테이블에서 정수장마다 2025년 매월 수질 검사 결과를 알 수 있다.

정수장과 행정구역의 관계는 N:M 관계이다.  
하나의 정수장에서 여러 행정구역에 물을 급수하고, 2개 이상의 정수장에서 하나의 행정구역으로 물을 공급하기도 한다.

---
### 이상치 검증
먹는 물 수질 기준으로 식수에 적합한지 확인  
pH : 5.8 ~ 8.5  
탁도 : 0.5 NTU 이하  
잔류염소 : 0.1 ~ 4.0 mg/L

---
## 환경 변수
기본값은 저장시스템 실습과 같은 비밀번호 `1234`

```bash
set WATER_DB_URL = postgresql://postgres:1234@localhost:5432/water_DB
```
---
## 요구사항에 대한 방향

### 한계
- 데이터 : 모든 데이터가 이상치 조건을 매우 높은 수치로 통과하고 각 값들의 편차가 크지 않다.
- 테이블 : 이 과제에서는 water 테이블만 사용한다. area 테이블은 이 과제에서는 사용하지 않는다.
- 배치 처리 : 정수장 및 구분별로 분기별 3가지 값의 평균값을 정리한다
- 이벤트 처리 : 잔류염소가 0.74 초과인 값들을 탐지하는 것으로 한다.
- 설명 : 이벤트 처리 데이터도 수질 기준의 상한을 매우 여유 있게 통과하는 값이라는 것을 명시한다.
---

## 파일 설명

| 파일명 | 설명 |
| --- | --- |
| `config.py` | DB 접속정보 환경변수 설정 |
| `database.py` | engine 생성 및 공통 유틸리티 |
| `batch_processor.py` | 배치 처리 : 각 정수장 및 구분별 분기별 평균 |
| `event_processor.py` | 이벤트 처리 : 잔류염소 0.74초과 |
| `pipeline.py` | 전체 통합 실행 |
| `verify_processing.py` | 처리 결과 검증 |
| `README.md` | 저장된 테이블 설명 및 한계, 처리시스템 설계, 실행 방법, 검증 SQL 정리 |
| `09_빅데이터처리시스템개발_김동욱.pptx` | 평가 결과 및 캡처 정리 자료 |

---

## 실행 방법

```bash
python pipeline.py # 파일 실행
```
---
## 결과

### 테이블
| 결과 | 결과 테이블 |
| --- | --- |
| water_DB | batch_water_summary |
| water_DB | event_water_chlorine_alert |

### batch_water_summary 테이블 구조

| 컬럼명 | 자료형 | 설명 |
| --- | --- | --- |
| `정수장` | String(10) | 정수장명 |
| `구분` | String(10) | 정수장 구분 |
| `ph_평균` | Numeric | 해당 분기의 pH 평균 (소수점 둘째 자리 반올림) |
| `탁도_평균` | Numeric | 해당 분기의 탁도 평균 (소수점 둘째 자리 반올림) |
| `잔류염소_평균` | Numeric | 해당 분기의 잔류염소 평균 (소수점 둘째 자리 반올림) |
| `분기` | Integer | 검사시기에서 추출한 분기 |
| `표본개수` | Integer | 해당 분기에 포함된 건수 |

### event_water_chlorine_alert 테이블 구조
| 컬럼명 | 자료형 | 설명 |
| --- | --- | --- |
| `id` | BigInteger | 대리키 |
| `event_type` | String(50) | 이벤트 종류 (`'WATER_EVENT'` 고정값) |
| `정수장` | String(10) | 정수장명 |
| `구분` | String(10) | 정수장 구분 |
| `ph` | Numeric(5,2) | pH농도 |
| `탁도` | Numeric(5,2) | 탁도 |
| `잔류염소` | Numeric(5,2) | 잔류염소 |
| `검사시기` | Date | 검사 연-월-일(일은 1로 고정) |
| `잔류염소_기준값` | Numeric(5,2) | 이벤트 기준값(0.74) |
| `이벤트_시간` | Timestamp | 이벤트 처리 시간 |

## 확인 SQL

```sql
SELECT COUNT(*) FROM batch_water_summary;
SELECT * FROM batch_water_summary ORDER BY 분기 ASC;
```

```sql
SELECT COUNT(*) FROM event_water_chlorine_alert;
SELECT * FROM event_water_chlorine_alert ORDER BY 잔류염소 DESC;
```
