import streamlit as st
import pandas as pd

st.title('CSV 데이터 필터링 앱')
file = st.file_uploader(
    'CSV 파일을 업로드 하세요',
    type='csv',
    accept_multiple_files=False
)

if file is not None:
    df = pd.read_csv(file)
    st.write(df)
    multi_columns = st.multiselect(
        '확인하고 싶은 열을 선택하세요',
        df.columns
    )
    filter_column = st.selectbox(
        '범위로 필터링할 열을 선택하세요',
        df.columns
    )
    min_value, max_value = st.slider(
        f'{filter_column} 범위 선택',
        df[filter_column].min(),
        df[filter_column].max(),
        value=(df[filter_column].min(), df[filter_column].max()),
    )

    st.divider()
    filtered_df = df.loc[(df[filter_column] >= min_value) & (df[filter_column] <= max_value), multi_columns]
    st.write(f'필터링 결과 ({len(filtered_df)}건)')
    st.write(filtered_df)

    
else:
    custom_css = """
    <style>
    /* st.code 박스 전체와 내부 pre, code 태그 배경색 변경 */
    .stCode, .stCode pre, .stCode code {
        background-color: #E0F7FA; /* 밝은 하늘색 */
        color: #01579B;           
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.code("CSV 파일을 업로드 해주세요.", language="text")