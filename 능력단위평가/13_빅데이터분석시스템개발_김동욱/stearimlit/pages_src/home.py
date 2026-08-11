import streamlit as st
import matplotlib.pyplot as plt
from data_loader import load_batter

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("🏏KBO 타자 분석 대시보드")

df = load_batter()

with st.sidebar:
    st.header("데이터 요약 필터")

    all_teams = sorted(df["팀"].unique())

    picked = st.multiselect("요약에 포함할 팀", options=all_teams, default=all_teams,)
    min_pa_only = st.checkbox("100타석 이상만 보기")

# 사이드바 조건 적용
summary_df = df[df['팀'].isin(picked)] if picked else df.iloc[0:0]
if min_pa_only:
    summary_df = summary_df[summary_df["타석"] >= 100]

# --- 본문 ----
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("선택된 팀 수", f"{len(picked)}개")
with col2:
    total_players = int(summary_df["선수"].nunique())
    st.metric("전체 선수 수(선택 기준)", f"{total_players}명")
with col3:
    st.metric("데이터 기간", "2025년도 정규시즌")

st.divider()

# --- 탭 ---
tab1, tab2 = st.tabs(["표로 보기", "그래프로 보기"])
with tab1:
    st.dataframe(
        summary_df.sort_values("타석", ascending=False).head(30)[["선수", "팀", "타율", "경기", "타석", "안타", "홈런", "출루율", "장타율"]], hide_index=True
    )
with tab2:
    if not summary_df.empty:
        chart_data = (
            summary_df.groupby("팀", observed=True)["OPS"].mean().sort_values(ascending=False)
        )
        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(chart_data.index, chart_data.values, color="#1f77b4")
        ax.set_xticks(range(len(chart_data)))
        ax.set_xticklabels(chart_data.index, rotation=0, ha="center")
        ax.set_title("팀별 OPS 평균")
        fig.tight_layout()
        st.pyplot(fig, use_container_width=False)
    else:
        st.info("사이드바에서 팀을 하나 이상 선택해주세요.")