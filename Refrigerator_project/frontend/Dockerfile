FROM python:3.12-slim

# 컨테이너 내부 작업 폴더
WORKDIR /app

# 패키지 목록 복사
COPY requirements.txt .

# 필요한 Python 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# Streamlit 파일 복사
COPY frontend/streamlit.py ./frontend/streamlit.py

# Streamlit 포트
EXPOSE 8501

# Streamlit 실행
CMD ["streamlit", "run", "frontend/streamlit.py", "--server.address=0.0.0.0", "--server.port=8501"]