import pandas as pd
import streamlit as st

from api_client import get_teams


st.title("🌎 국가대표팀")


search = st.text_input(
    "팀 검색",
    placeholder="예: 대한민국",
)


if st.button(
    "팀 조회",
    type="primary",
):

    try:
        data = get_teams(
            search=search or None
        )

        df = pd.DataFrame(data)

        if df.empty:
            st.warning(
                "검색된 팀이 없습니다."
            )

        else:
            st.dataframe(
                df,
                use_container_width=True,
                hide_index=True,
            )

    except Exception as e:
        st.error(str(e))
