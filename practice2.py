import streamlit as st
import pandas as pd

st.title('CSV 데이터 필터링 앱')

file = st.file_uploader(
    'CSV 파일을 업로드하세요',
    type='csv',
    accept_multiple_files=False
)

if file is not None:
    st.write('업로드 된 데이터 미리보기')
    df = pd.read_csv(file)
    st.write(df)
    
    st.divider()

    select_col = st.multiselect('확인하고 싶은 열을 선택하세요', df.columns)
    filter_col = st.selectbox('범위로 필터링할 열을 선택하세요', df.columns)

    if filter_col == '가격':
        min_price, max_price = st.slider(
            '가격 범위 선택',
            min_value=3000,
            max_value=6000,
            value=(3000, 6000),
            step=500
        )

        st.divider()

        result = df[(df[filter_col] >= min_price) & (df[filter_col] <= max_price)]
        result = result[select_col]
        st.text(f'필터링 결과 ({len(result)}건)')
        st.write(result)
else:
    st.write('CSV 파일을 업로드해주세요.')