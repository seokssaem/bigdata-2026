import pandas as pd
import streamlit as st

from api_client import get_players


st.title("🔎 선수 검색")

st.write(
    "선수 이름, 국가, 포지션 등을 이용해서 선수를 찾을 수 있습니다."
)


# -----------------------------
# 검색 폼
# -----------------------------
with st.form("player_search_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        search = st.text_input(
            "선수 이름",
            placeholder="예: '손흥민' or 'Son'" ,
        )

    with col2:
        team = st.text_input(
            "국가",
            placeholder="예: 대한민국",
        )

    with col3:
        position = st.selectbox(
            "포지션",
            [
                "전체",
                "GK",
                "DF",
                "MF",
                "FW",
            ],
        )

    col4, col5 = st.columns(2)

    with col4:
        sort_by = st.selectbox(
            "정렬 기준",
            [
                "player",
                "games",
                "age",
                "minutes",
                "goals",
                "assists",
            ],
            index=0,
        )

    with col5:
        sort_order = st.selectbox(
            "정렬 방향",
            [
                "asc",
                "desc",
            ],
        )

    submitted = st.form_submit_button(
        "🔎 검색",
        type="primary",
        use_container_width=True,
    )


# -----------------------------
# 검색 실행
# -----------------------------
if submitted:

    try:
        data = get_players(
            search=search or None,
            team=team or None,
            position=(
                None
                if position == "전체"
                else position
            ),
            sort_by=sort_by,
            sort_order=sort_order,
            page=1,
            size=100,
        )

        st.session_state.player_search_result = data

    except Exception as e:
        st.error(str(e))


# -----------------------------
# 검색 결과
# -----------------------------
data = st.session_state.get(
    "player_search_result",
    [],
)

if data:

    df = pd.DataFrame(data)

    st.divider()

    st.subheader(
        f"검색 결과 : {len(df)}명"
    )

    # 화면에 보여줄 컬럼
    display_columns = [
        column
        for column in [

            "player",
            "games",
            "age",
            "minutes",
            "goals",
            "assists",
        ]
        if column in df.columns
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True,
    )

    st.divider()

    st.subheader("선수 선택")

    # selectbox에 표시할 문자열
    player_options = {}

    for row in data:

        player_id = row.get("id")
        player_name = row.get(
            "player",
            "이름 없음",
        )
        player_team = row.get(
            "team",
            "-",
        )

        label = (
            f"{player_name} "
            f"({player_team}) "
            f"- ID {player_id}"
        )

        player_options[label] = player_id

    selected_label = st.selectbox(
        "상세 스탯을 볼 선수를 선택하세요.",
        list(player_options.keys()),
    )

    selected_id = player_options[
        selected_label
    ]

    if st.button(
        "👤 선수 상세 보기",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.selected_player_id = (
            selected_id
        )

        st.switch_page(
            "pages/player_detail.py"
        )

else:
    st.info(
        "검색 조건을 입력한 뒤 검색 버튼을 눌러주세요."
    )
