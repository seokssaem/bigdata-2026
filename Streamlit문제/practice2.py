import pandas as pd
import streamlit as st

st.title("CSV 데이터 필터링 앱")

file = st.file_uploader(
    "CSV 파일을 업로드하세요", type="csv", accept_multiple_files=False
)

if file is not None:
    df = pd.read_csv(file)

    st.write("업로드된 데이터 미리보기")
    st.dataframe(df)

    st.divider()

    selected_cols = st.multiselect(
        "확인하고 싶은 열을 선택하세요",
        options=df.columns.tolist(),
        default=["메뉴명"],
    )

    filter_options = df.columns.tolist()
    default_idx = filter_options.index("가격") if "가격" in filter_options else 0

    filter_col = st.selectbox(
        "범위로 필터링할 열을 선택하세요", options=filter_options, index=default_idx
    )

    min_val = int(df[filter_col].min())
    max_val = int(df[filter_col].max())

    selected_range = st.slider(
        f"{filter_col} 범위 선택",
        min_value=min_val,
        max_value=max_val,
        value=(min_val, max_val),
    )

    st.divider()

    filtered_df = df[
        (df[filter_col] >= selected_range[0])
        & (df[filter_col] <= selected_range[1])
    ]

    st.write(f"필터링 결과 ({len(filtered_df)}건)")
    st.dataframe(filtered_df[selected_cols] if selected_cols else filtered_df)

else:
    st.info("CSV 파일을 업로드해주세요.")