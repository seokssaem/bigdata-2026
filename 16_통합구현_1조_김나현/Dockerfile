# KOBIS API 기반 영화 정보 및 즐겨찾기 서비스 - Dockerfile
# db --> PostgreSQL 17
# api --> Fastapi
# web --> Steamlit
# api, web 두 서비스가 이 이미지 하나를 공유한다.

FROM python:3.12-slim

WORKDIR /app

# requirements.txt만 먼저 복사 --> 코드가 바뀌어도 패키지 설치 레이어는 캐시로 재사용
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY main.py .
COPY models.py .
COPY streamlit_app.py .

# database/ 폴더 추가
COPY database/ ./database/

# repositories/ 폴더 추가
COPY repositories/ ./repositories/

# routers/ 폴더 추가
COPY routers/ ./routers/

# schema/ 폴더 추가
COPY schema/ ./schema/

# services/ 폴더 추가
COPY services/ ./services/

# EXPOSE : 이 컨테이너가 몇 번 포트를 쓰는지 문서화하는 명령어(실제로 포트를 열어주는 건 아니다.)
# --> 실제 포트 연결은 docker-compose.yml이 담당
# 8000 --> Fastapi, 8501 --> streamlit
EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]