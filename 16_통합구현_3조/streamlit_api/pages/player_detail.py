import pandas as pd
import streamlit as st

from api_client import get_player


st.title("👤 선수 상세 스탯")


player_id = st.session_state.get(
    "selected_player_id"
)


# -----------------------------
# 선수가 선택되지 않은 경우
# -----------------------------
if player_id is None:

    st.warning(
        "선택된 선수가 없습니다."
    )

    st.write(
        "먼저 선수 검색 페이지에서 선수를 선택해주세요."
    )

    if st.button(
        "🔎 선수 검색으로 이동"
    ):
        st.switch_page(
            "pages/player_search.py"
        )

    st.stop()


# -----------------------------
# 선수 API 조회
# -----------------------------
try:
    player = get_player(
        player_id
    )

except Exception as e:
    st.error(str(e))
    st.stop()


# -----------------------------
# 기본 정보
# -----------------------------
player_name = player.get(
    "player",
    "이름 없음",
)

team = player.get(
    "team",
    "-",
)

position = player.get(
    "position",
    "-",
)

age = player.get(
    "age",
    "-",
)

club = player.get(
    "club",
    "-",
)


st.header(
    f"⚽ {player_name}"
)

st.caption(
    f"{team} · {position}"
)


col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "국가",
        team,
    )

with col2:
    st.metric(
        "포지션",
        position,
    )

with col3:
    st.metric(
        "나이",
        age,
    )

with col4:
    st.metric(
        "소속팀",
        club,
    )


st.divider()


# -----------------------------
# 주요 기록
# -----------------------------
st.subheader("📊 주요 기록")


games = player.get(
    "games",
    0,
)

goals = player.get(
    "goals",
    0,
)

assists = player.get(
    "assists",
    0,
)


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "출전",
        games,
    )

with col2:
    st.metric(
        "득점",
        goals,
    )

with col3:
    st.metric(
        "도움",
        assists,
    )


# -----------------------------
# 계산 통계
# -----------------------------
st.divider()

st.subheader("📈 계산 스탯")


if games and games > 0:

    goals_per_game = round(
        goals / games,
        2,
    )

    assists_per_game = round(
        assists / games,
        2,
    )

    attack_points_per_game = round(
        (goals + assists) / games,
        2,
    )

else:
    goals_per_game = 0
    assists_per_game = 0
    attack_points_per_game = 0


col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "경기당 득점",
        goals_per_game,
    )

with col2:
    st.metric(
        "경기당 도움",
        assists_per_game,
    )

with col3:
    st.metric(
        "경기당 공격포인트",
        attack_points_per_game,
    )


# -----------------------------
# 차트
# -----------------------------
st.divider()

st.subheader("📊 공격 기록 비교")


chart_df = pd.DataFrame(
    {
        "기록": [
            "득점",
            "도움",
        ],
        "값": [
            goals,
            assists,
        ],
    }
)


st.bar_chart(
    chart_df,
    x="기록",
    y="값",
)


# -----------------------------
# 원본 데이터
# -----------------------------
with st.expander(
    "전체 선수 데이터 보기"
):
    st.json(player)


st.divider()


# -----------------------------
# 다시 검색
# -----------------------------
if st.button(
    "← 선수 검색으로 돌아가기"
):
    st.switch_page(
        "pages/player_search.py"
    )