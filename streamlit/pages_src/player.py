import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_loader import load_batter

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("선수 기록 조회")

# 데이터 불러오기
df = load_batter()
player_list = sorted(df["선수"].unique())

if "favorite_players" not in st.session_state:
    st.session_state.favorite_players = []

st.subheader("즐겨찾는 선수 관리")

col_add, col_btn = st.columns([3, 1])
with col_add:
    player_to_add = st.selectbox("추가할 선수", player_list, key="player_to_add")
with col_btn:
    st.write(" ")
    st.write(" ")
    if st.button("+ 추가"):
        if player_to_add not in st.session_state.favorite_players:
            st.session_state.favorite_players.append(player_to_add)
            st.rerun()

if not st.session_state.favorite_players:
    st.info("아직 즐겨찾기에 추가한 선수가 없습니다. 위에서 선수를 선택하고 추가 버튼을 눌러보세요.")
else:
    for i, player in enumerate(st.session_state.favorite_players):
        col_name, col_del = st.columns([4, 1])
        with col_name:
            st.write(f'{i+1}. {player}')
        with col_del:
            if st.button('삭제', key=f'del_{i}'):
                st.session_state.favorite_players.pop(i)
                st.rerun()


st.divider()

# --- 즐겨찾기한 선수들의 "기본 기록" 비교 ---
if st.session_state.favorite_players:
    st.write("비교할 선수 선택 (최대 5명)")
    focus_players = st.pills(
        "선수 선택",
        options=st.session_state.favorite_players,
        selection_mode="multi",
        default=st.session_state.favorite_players[:1],
        label_visibility="collapsed",
    )

    if len(focus_players) > 5:
        st.warning("최대 5명까지 비교할 수 있습니다. 앞의 5명만 표시합니다.")
        focus_players = focus_players[:5]

    if not focus_players:
        st.info("위에서 선수를 하나 이상 선택해주세요.")
    else:
        compare_df = df[df["선수"].isin(focus_players)].set_index("선수")

        def grouped_bar_chart(data: pd.DataFrame, title: str):
            # data: 인덱스=선수, 컬럼=지표
            indicators = data.columns.tolist()
            players = data.index.tolist()

            x = np.arange(len(indicators))
            width = 0.8 / len(players)

            fig, ax = plt.subplots(figsize=(6, 4))
            for i, player in enumerate(players):
                offset = (i - (len(players) - 1) / 2) * width
                ax.bar(x + offset, data.loc[player], width=width, label=player)

            ax.set_xticks(x)
            ax.set_xticklabels(indicators, rotation=0, ha="center")
            ax.set_title(title)
            ax.legend()
            fig.tight_layout()
            st.pyplot(fig, use_container_width=False)

        col_count, col_ratio = st.columns(2)
        with col_count:
            st.subheader("선수 비교 - 카운트 지표")
            grouped_bar_chart(compare_df[["경기", "타석", "안타", "홈런"]], "카운트 지표 비교")
        with col_ratio:
            st.subheader("선수 비교 - 비율 지표")
            grouped_bar_chart(compare_df[["타율", "출루율", "장타율"]], "비율 지표 비교")

        st.subheader("상세 수치")
        st.dataframe(
            compare_df[["팀", "경기", "타석", "안타", "홈런", "타율", "출루율", "장타율"]],
            hide_index=False,
        )