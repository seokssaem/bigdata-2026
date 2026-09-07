FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY main.py .
COPY models.py .
COPY auth ./auth
COPY data ./data
COPY database ./database
COPY routers ./routers
COPY schema ./schema

# Fastapi 포트 번호
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]