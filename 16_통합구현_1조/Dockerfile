# movie1 - Dockerfile

FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 전체 복사
COPY main.py .
COPY models.py .
COPY streamlit_app.py .
COPY database/ ./database/
COPY repositories/ ./repositories/
COPY services/ ./services/
COPY routers/ ./routers/
COPY schema/ ./schema/

EXPOSE 8000
EXPOSE 8501

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
