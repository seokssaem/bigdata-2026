import pandas as pd
import streamlit as st

from api_client import get_matches


st.title("🏟️ 경기 검색")


col1, col2 = st.columns(2)

with col1:
    team = st.text_input(
        "국가",
        placeholder="예: 대한민국",
    )

with col2:
    round_name = st.text_input(
        "라운드",
        placeholder="예: Group Stage",
    )


if st.button(
    "경기 조회",
    type="primary",
):

    try:
        data = get_matches(
            team=team or None,
            round_name=round_name or None,
        )

        df = pd.DataFrame(data)

        if df.empty:
            st.warning(
                "검색된 경기가 없습니다."
            )

        else:
            st.success(
                f"{len(df)}경기를 찾았습니다."
            )

            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

    except Exception as e:
        st.error(str(e))
