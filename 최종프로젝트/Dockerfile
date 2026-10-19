# 생필품 가격 리포트 - Dockerfile
# FastAPI 앱 하나를 담는 이미지. (DB는 docker-compose.yml 의 db 컨테이너가 따로 맡는다)

FROM python:3.12-slim

# 그래프(matplotlib)에 한글("원" 등)이 나오도록 한글 글꼴(나눔고딕)을 설치한다.
# slim 이미지에는 글꼴이 없어서, 안 깔면 그래프의 한글이 네모(□)로 깨진다.
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-nanum \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# requirements.txt 만 먼저 복사 --> 코드가 바뀌어도 패키지 설치 단계는 캐시를 재사용한다
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 글꼴 목록(캐시)을 미리 만들어 둔다. 안 하면 첫 그래프 요청이 몇 초 느려진다.
RUN python -c "import matplotlib.pyplot"

# 서버가 실제로 쓰는 코드만 복사한다 (데이터 파일, .env 등은 복사하지 않는다)
COPY main.py database.py models.py security.py templates_config.py ./
COPY routers/ ./routers/
COPY schemas/ ./schemas/
COPY templates/ ./templates/
COPY static/ ./static/

# EXPOSE: 이 컨테이너가 8000번 포트를 쓴다고 알려주는 문서 역할 (실제 연결은 docker-compose.yml)
EXPOSE 8000

# --host 0.0.0.0 : 컨테이너 밖에서도 접속할 수 있게 연다
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
