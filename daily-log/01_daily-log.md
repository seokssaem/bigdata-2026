# 학습일지 (daily-log.md)

## 작성자

* 이름: 김나현

---

## 2026-06-12

### 오늘 개별 공부한 것들

- FastAPI CRUD 복습
- field_validator 복습
```
@field_validator('price')
@classmethod
def price_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('가격은 0보다 커야 합니다.')
        return v
```

- jlpt n3 공부

### 비고
- jlpt 공부를 함께 진행할 것같습니다. (7월 5일 시험)
