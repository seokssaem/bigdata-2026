import streamlit as st

from api_client import BASE_URL, health_check


st.title("⚽ 2026 FIFA 월드컵 데이터")
st.subheader("World Cup Data Dashboard")

st.write(
    """
    PostgreSQL에 저장된 월드컵 데이터를 FastAPI로 조회하고
    Streamlit에서 검색·분석하는 프로젝트입니다.
    """
)


# -----------------------------
# 서버 상태
# -----------------------------
try:
    if health_check():
        st.success("✅ FastAPI 서버 연결 성공")
    else:
        st.error("❌ FastAPI 서버 연결 실패")
except Exception:
    st.error(
        "FastAPI 서버가 실행되어 있지 않습니다. "
        "`uvicorn main:app --reload`를 먼저 실행하세요."
    )


st.divider()


# -----------------------------
# 프로젝트 설명
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "DATABASE",
        "PostgreSQL",
    )

with col2:
    st.metric(
        "BACKEND",
        "FastAPI",
    )

with col3:
    st.metric(
        "FRONTEND",
        "Streamlit",
    )


st.divider()

st.markdown(
    """
    ### 사용 방법

    **1. 선수 검색**

    상단 메뉴의 `선수 검색`에서 선수 이름이나 국가를 검색합니다.

    **2. 선수 선택**

    검색 결과에서 원하는 선수를 선택합니다.

    **3. 상세 스탯 확인**

    `선수 상세 보기` 버튼을 누르면 해당 선수의 상세 페이지로 이동합니다.

    **4. 통계**

    월드컵 최종 성적 / 선수득점 통계를 확인할 수 있습니다.
    """
)

st.info(
    f"FastAPI 주소: {BASE_URL}"
)
