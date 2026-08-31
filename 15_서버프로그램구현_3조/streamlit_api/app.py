import streamlit as st


st.set_page_config(
    page_title="2026 FIFA 월드컵",
    page_icon="⚽",
    layout="wide",
)


if "selected_player_id" not in st.session_state:
    st.session_state.selected_player_id = None


home_page = st.Page(
    "pages/home.py",
    title="홈",
    icon="🏠",
    default=True,
)

player_search_page = st.Page(
    "pages/player_search.py",
    title="선수 검색",
    icon="🔎",
)

player_detail_page = st.Page(
    "pages/player_detail.py",
    title="선수 상세",
    icon="👤",
)

matches_page = st.Page(
    "pages/matches.py",
    title="경기",
    icon="🥅",
)

teams_page = st.Page(
    "pages/teams.py",
    title="팀",
    icon="👕",
)

stats_page = st.Page(
    "pages/stats.py",
    title="통계",
    icon="📊",
)


navigation = st.navigation(
    [
        home_page,
        player_search_page,
        player_detail_page,
        matches_page,
        teams_page,
        stats_page,
    ],
    position="top",
)


navigation.run()
