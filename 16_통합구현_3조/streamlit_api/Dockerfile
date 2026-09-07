FROM python:3.12-slim

WORKDIR /web

COPY streamlit_api/requirements_streamlit.txt .
RUN pip install --no-cache-dir -r requirements_streamlit.txt

COPY data ./data
COPY streamlit_api/pages ./pages
COPY streamlit_api/api_client.py .
COPY streamlit_api/app.py .

# streamlit 포트 번호
EXPOSE 8501


# api Dockerfile과 비슷한 형태로 작성 -> "--server.address=0.0.0.0", "--server.port=8501" 로 수정
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]