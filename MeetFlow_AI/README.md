# MeetFlow AI

AI 기반 스마트 회의 및 업무 관리 플랫폼

## 1. 프로젝트 개요

MeetFlow AI는 회의 내용을 기록하고 인공지능으로 분석하여 회의록, 요약, 결정사항, 담당 업무 및 마감일을 관리하는 웹 플랫폼이다.

- 프로젝트 유형: NCS 빅데이터 분석 플랫폼 개발자 양성과정 최종 팀 프로젝트
- 팀원: 김시현, 홍은경
- 배포 주소: https://aimeetflow.duckdns.org/views
- 소스코드: https://github.com/eunkyeongc/MeetFlow-AI

## 2. 문제 정의

일반적인 회의에서는 회의 내용을 기록한 후 주요 결정사항과 후속 업무를 별도로 정리해야 한다.

- 회의록 작성에 많은 시간이 소요된다.
- 주요 결정사항과 담당 업무가 누락될 수 있다.
- 업무 담당자와 마감일을 체계적으로 관리하기 어렵다.
- 회의 기록과 실제 업무 관리가 분리되어 있다.

MeetFlow AI는 회의 기록부터 AI 분석, 업무 관리까지 연결하여 이러한 문제를 해결하는 것을 목표로 한다.

## 3. 주요 기능

### 3.1 회의 입력

- 텍스트 직접 입력
- 회의 음성 파일 업로드
- 웹 브라우저에서 실시간 녹음

### 3.2 AI 회의 분석

- STT (Speech-to-Text): 음성을 텍스트로 변환
- LLM (Large Language Model): 회의 내용 분석
- 회의 요약 및 주요 안건 정리
- 결정사항 추출
- 담당자, 업무 및 마감일 추출

### 3.3 회의 및 업무 관리

- 프로젝트 생성 및 관리
- 회의록 조회 및 관리
- 업무 등록 및 진행 상태 관리
- 캘린더를 통한 일정 확인
- 대시보드를 통한 업무 현황 확인

### 3.4 사용자 인증 및 공유

- 회원가입 및 로그인
- JWT (JSON Web Token) 기반 인증
- 프로젝트 멤버 관리
- 회의 참여자 관리
- 사용자별 접근 권한 검증
- 동명이인 구분을 위한 이메일 정보 활용

## 4. 시스템 구성도

```text
사용자 웹 브라우저
        |
        v
Nginx / HTTPS
        |
        v
FastAPI 애플리케이션
        |
        +---- 사용자 인증 및 권한 관리
        |
        +---- 프로젝트 / 회의 / 업무 관리
        |
        +---- 음성 파일 처리 ----> OpenAI STT API
        |
        +---- 회의 내용 분석 ----> OpenAI LLM API
        |
        v
PostgreSQL 데이터베이스
```

배포 환경에서는 AWS Lightsail의 Ubuntu 서버에서 Docker Compose를 이용하여 FastAPI와 PostgreSQL 컨테이너를 운영한다.

## 5. 기술 스택

| 구분 | 기술 |
|---|---|
| Backend | Python 3.11, FastAPI |
| Database | PostgreSQL 17 |
| ORM (Object-Relational Mapping) | SQLAlchemy |
| Data Validation | Pydantic |
| Authentication | JWT (JSON Web Token) |
| Frontend | HTML, CSS, JavaScript, Jinja2 |
| AI Analysis | OpenAI API, gpt-4.1-mini |
| STT (Speech-to-Text) | OpenAI API, gpt-4o-mini-transcribe |
| Container | Docker, Docker Compose |
| Deployment | AWS Lightsail, Ubuntu, Nginx |
| HTTPS | DuckDNS, Let's Encrypt |
| Test | pytest |
| CI (Continuous Integration) | GitHub Actions |

## 6. 프로젝트 구조

```text
meetflow_ai/
├── .github/
│   └── workflows/
│       └── ci.yml
├── .dockerignore
├── .env                 # 로컬 전용, GitHub 제출 제외
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
├── TROUBLESHOOTING.md
├── frequency_commands.md
├── main.py
├── database.py
├── models.py
│
├── migrations/
│   └── 001_add_users_profile_image.sql
│
├── routers/
│   ├── __init__.py
│   ├── auth.py
│   ├── meetings.py
│   ├── profile.py
│   ├── projects.py
│   ├── tasks.py
│   ├── users.py
│   └── views.py
│
├── schemas/
│   ├── __init__.py
│   ├── meeting.py
│   ├── project.py
│   ├── task.py
│   └── user.py
│
├── services/
│   ├── __init__.py
│   ├── ai_service.py
│   ├── auth_service.py
│   ├── calendar_service.py
│   ├── password_service.py
│   └── stt_service.py
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
├── templates/
│   ├── base.html
│   ├── calendar.html
│   ├── dashboard.html
│   ├── login.html
│   ├── meeting_detail.html
│   ├── meetings.html
│   ├── new_meeting.html
│   ├── new_task.html
│   └── register.html
│
├── tests/
│   ├── __init__.py
│   ├── test_ai.py
│   └── test_meetings.py
│
└── uploads/
    ├── audio/
    └── profile/
```

## 7. 설치 및 실행 방법

### 7.1 사전 준비

- Git
- Docker 및 Docker Compose
- OpenAI API 키

### 7.2 프로젝트 다운로드

```bash
git clone https://github.com/eunkyeongc/MeetFlow-AI.git
cd MeetFlow-AI
```

### 7.3 환경변수 설정

```bash
cp .env.example .env
```

`.env` 파일에서 PostgreSQL 비밀번호, JWT 비밀키, OpenAI API 키 등을 실제 실행 환경에 맞게 설정한다. `.env`에는 인증정보가 포함될 수 있으므로 GitHub에 업로드하지 않는다.

### 7.4 Docker 실행

```bash
docker compose up -d --build
```

컨테이너 상태 확인:

```bash
docker compose ps
```

로그 확인:

```bash
docker compose logs -f api
```

### 7.5 접속 주소

로컬 Docker 환경:

- 웹 화면: http://localhost:8000/views
- API 문서: http://localhost:8000/docs
- API 상태 확인: http://localhost:8000/

실제 배포 환경:

- https://aimeetflow.duckdns.org/views

## 8. 데이터베이스

| 테이블 | 용도 |
|---|---|
| users | 사용자 정보 |
| projects | 프로젝트 정보 |
| project_members | 프로젝트 참여자 |
| meetings | 회의 정보 |
| meeting_participants | 회의 참여자 |
| tasks | 업무 정보 |

SQLAlchemy 모델을 통해 데이터베이스 테이블을 정의하고 관계형 데이터를 관리한다.

## 9. 테스트 및 CI

테스트 프레임워크로 pytest를 사용한다.

```bash
python -m pytest -v
```

GitHub Actions를 통해 소스코드 변경 시 자동 테스트를 수행한다.

최근 확인된 테스트 결과:

- 총 28개 테스트 통과
- GitHub Actions 실행 성공

## 10. 실행 결과 및 기대 효과

```text
회의 내용 입력
    ↓
음성인 경우 STT 변환
    ↓
AI 회의 분석
    ↓
회의 요약 / 결정사항 / 담당 업무 추출
    ↓
회의 및 업무 데이터 저장
    ↓
대시보드 / 캘린더에서 관리
```

회의 기록과 후속 업무 관리를 연결하고, 반복적인 회의록 정리 작업을 줄이는 것을 목표로 한다.

## 11. 팀원별 역할

### 김시현

- 데이터베이스 설계 및 구성
- Python 및 Docker 개발 환경 구성
- Docker 컨테이너 관련 작업
- pytest 테스트 관련 작업
- Jinja2 기반 사용자 화면 구현

### 홍은경

- JWT 인증 기능 구현
- STT 및 LLM 기반 AI 분석 기능 구현
- JavaScript 기반 사용자 화면 기능 구현
- GitHub Actions 테스트 자동화
- AWS Lightsail 서버 배포 및 HTTPS 환경 구성

## 12. 트러블슈팅

개발 과정에서 발생한 주요 오류와 해결 과정은 `TROUBLESHOOTING.md` 문서에 별도로 기록한다.

## 13. 향후 개선 방향

- AI 분석 결과의 정확도 향상
- 회의 및 업무 검색 기능 강화
- 사용자 편의성 개선
- 업무 알림 및 외부 일정 연동 기능 확장
