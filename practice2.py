# 2. CSV 데이터 필터링
import streamlit as st
import pandas as pd

file = st.file_uploader(
    'csv파일을 업로드하세요',
    type='csv',
    accept_multiple_files=False
)

if file is not None:
    st.write('업로드된 파일 미리보기')
    df = pd.read_csv(file)
    st.write(df)

    st.divider()

    Q1 = st.multiselect(
        '확인하고 싶은 열을 선택하세요',
        ['메뉴명', 'Unnamed: 0', '가격']
    )
    Q2 = st.selectbox(
        '범위로 필터링할 열을 선택하세요',
        ['Unnamed: 0', '가격']
    )    
    correct = '가격'

    min_price, max_price = st.slider(
        '가격 범위 선택',
        min_value=4500,
        max_value=6000,
        value=(4500,6000)
    )

    filtered_df = df[
            (df[Q2] >= min_price) &
            (df[Q2] <= max_price)
        ]


st.divider()

st.write(f"필터링 결과 ({len(filtered_df)}건)")

if Q1:
    st.dataframe(filtered_df[Q1])
else:
    st.warning("표시할 열을 선택하세요.")