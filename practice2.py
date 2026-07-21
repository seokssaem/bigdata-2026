# =============================================================
# ~/bigdata202/fastapi//Streamlit/practice2.py
#
#  Streamlit 라이브러리 기초 연습문제 / 실행 할 때 터미널 streamlit run [파일명] 
#
# ===========================================================
import streamlit as st
import pandas as pd

# 1. CSV 데이터 필터링 앱
st.title('CSV 데이터 필터링 앱')

file = st.file_uploader(
    'CSV파일을 업로드 하세요',
    type='csv',
    accept_multiple_files=False
)
st.text('업로드된 데이터 미리보기')

if file is not None:
    df = pd.read_csv(file)
    st.write(df)

st.divider()

menu1 = st.multiselect(
    '확인하고 싶은 열을 선택하세요',
    ["메뉴명", "가격"]
)

menu2 = st.multiselect(
    '범위로 필터링할 열을 선택하세요',
    ["메뉴명", "가격"]
)

start_price, end_price = st.slider(
    '가격 범위 선택',
    min_value=4500,
    max_value=6000,
    value=(4500, 6000)
)

st.divider()

all_menus = [
    {"메뉴명": "아메리카노", "가격": 4500},
    {"메뉴명": "카페라떼", "가격": 5000},
    {"메뉴명": "카푸치노", "가격": 5500},
    {"메뉴명": "말차라떼", "가격": 6000}
]

