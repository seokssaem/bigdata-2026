FROM python:3.12-slim

# 컨테이너 내부 작업 폴더
WORKDIR /app

# requirements.txt 먼저 복사
COPY requirements.txt .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# FastAPI 컨테이너에 필요한 파일만 복사
COPY main.py .
COPY database.py .
COPY models.py .
COPY routers/ ./routers
COPY schema/ ./schema

# FastAPI 포트
EXPOSE 8000

# FastAPI 실행
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]