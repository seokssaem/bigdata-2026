import sys
import os
import streamlit as st

# --- 경로 설정 ---
sys.path.append(os.path.join(os.path.dirname(__file__), "pages_src"))

st.set_page_config(
    page_title="KBO 타자 분석 대시보드",
    page_icon="⚾️",
    layout="wide"
)

# --- 페이지 등록 ---
home_page = st.Page("pages_src/home.py", title="홈", default=True)
player_page = st.Page("pages_src/player.py", title="선수 기록 조회")
histogram_page = st.Page("pages_src/histogram.py", title="히스토그램 분석")
hypothesis_page = st.Page("pages_src/hypothesis_test.py", title="가설 검증 및 통계 분석")
model_page = st.Page("pages_src/model_predict.py", title="OPS 예측 모델")
about_page = st.Page("pages_src/about.py", title="소개")

pg = st.navigation({
    "메인": [home_page],
    "데이터 탐색": [player_page, histogram_page, hypothesis_page, model_page],
    "기타": [about_page]
})

# -- 실행 --
pg.run()