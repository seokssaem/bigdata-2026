# 학습일지 (daily-log.md)

## 작성자
* 이름 : 태두혁

---

## 2026-06-15
- FATSAPI 블로그 포스트 검색, 생성, 수정 및 삭제 기능 복습
- HTMI/CSS 수업 내용 복습
    https://github.com/TaeGaori/fastapi_2026/tree/main/blog


## 2026-06-16
- FASTAPI 오늘 뭐먹지?? 복습
    https://github.com/TaeGaori/fastapi_2026/blob/main/%EC%8B%A4%EC%8A%B5/07_%EC%A0%90%EC%8B%AC%EB%A9%94%EB%89%B4.py

## 2026-06-17
- 토이 프로젝트 게임 캐릭터 만들기
    https://github.com/TaeGaori/bigdata-basic/blob/main/Practice/Toy_Project.py
    

## 2026-06-18
- fastapi -> routers(회원가입) 복습
    https://github.com/TaeGaori/fastapi_2026/tree/main/routers

## 2026-06-17
- html + css를 활용하여 대시보드 웹페이지 만들기 복습

## 2026-06-22
- html 애니매이션을 활용하기 
    - translate     (현재 위치에서 x,y축으로 이동)
    - scale         (확대 or 축소)
    - rotate        (중심축 기준으로 회전)
    - perpective    (3D변형할 때입체감)
    - skew          (비틀거나 기울임)
    - product       ()
    - animation     (시간에 따라 변화시킴)

## 2026-06-23
- html총 정리 (원두 사이트)
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%84%B7%ED%94%8C%20%EB%94%B0%EB%9D%BC%ED%95%98%EA%B8%B0/stylc.css

## 2026-06-24
- SQLE 기초 공부
    SELECT   컬럼명           -- 1. 뭘 볼지
    FROM     테이블명          -- 2. 어디서
    WHERE    조건             -- 3. 어떤 조건으로
    GROUP BY 그룹기준          -- 4. 어떻게 묶을지
    HAVING   그룹조건          -- 5. 묶은 결과 조건
    ORDER BY 정렬기준          -- 6. 어떻게 정렬할지
    LIMIT    숫자             -- 7. 몇 개만 볼지

    안 쓰는 건 가능하지만 사용한다면 순서 지키기!


- html 원두 사이트를 활용하여 나만의 페이지로 편집
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/index.html
    https://github.com/TaeGaori/html_css_js/blob/main/%EB%82%98%EB%A7%8C%EC%9D%98%20%ED%8E%98%EC%9D%B4%EC%A7%80/stylc.css


## 2026-06-25
- SQLD JOIN을 사용하여 두 테이블 연결하기

## 2026-06-26
- SQLD  시험에 나올 기출문제 실습 및 연습문제 풀기

## 2026-06-29
- fastapi 복습
    - CRUD --> 데이터를 다루는 4가지 기본 동작
        -Create : 생성 POST(Fastapi) INSERT(SQL)     --> ex.회원가입, 글 작성
        -Read   : 조회 GET(FastAPI) SELECT(SQL)      --> ex.목록 보기, 상세 보기
        -Update : 수정 PUT/PATCH(FastAPI) UPDATE(SQL)--> ex.정보 수정
        -Delete : 삭제 DELETE(FastAPI) DELETE(SQL)   --> ex. 회원 탈퇴, 글 삭제

    - sql_databases --> User + Item, 1:N 관계 CRUD
        - 공식 FastAPI 튜토리얼 예제를 PostgreSQL로 변환한 버전
        - 'User'(사용자)가 여러 개의 'Item' (아이템)을 소유하는 **1:N** 구조
        - 'crud.py'를 별도로 분리하여 DB 조작 로직과 라우터 로직을 나눔
    
    - __init__.py 생성 이유:  오류 방지


## 2026-06-30
- 판다스를 활용하여 엑셀 파일 읽고 병합 + 시각화

- fastapi로 main 테스트하기.
        pytest 라이브러리 --> python 표준 테스트 도구
        파일과 함수 이름은 test_로 시작
        권장사항 > 테스트 DB도 따로 만들어준다.
        uv add pytest --> 설치  