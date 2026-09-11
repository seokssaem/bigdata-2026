from pathlib import Path

import pandas as pd
import streamlit as st

from api_client import get_top_scorers

# =========================================================
# 페이지 기본 설정
# =========================================================

st.title("📊 월드컵 통계")

tab1, tab2 = st.tabs(
    [
        "🏆 월드컵 최종 순위",
        "⚽ 선수 득점 통계",
    ]
)

# =========================================================
# 경기 CSV 불러오기
# =========================================================

def load_matches():

    # 현재 파일:
    # streamlit_app/pages/stats.py
    #
    # parents[2]:
    # 프로젝트 최상위 폴더

    project_root = (
        Path(__file__)
        .resolve()
        .parents[2]
    )

    matches_file = (
        project_root
        / "data"
        / "matches.csv"
    )

    if not matches_file.exists():

        raise FileNotFoundError(
            "data/matches.csv 파일을 찾을 수 없습니다."
        )


    df = pd.read_csv(
        matches_file
    )

    # -----------------------------------------------------
    # 반드시 필요한 컬럼
    # -----------------------------------------------------

    required_columns = [
        "round",
        "home_team",
        "away_team",
        "home_score",
        "away_score",
    ]

    missing_columns = [
        column
        for column in required_columns
        if column not in df.columns
    ]

    if missing_columns:

        raise ValueError(
            "matches.csv에 필요한 컬럼이 없습니다: "
            + ", ".join(missing_columns)
        )

    # -----------------------------------------------------
    # 숫자형 컬럼 변환
    # -----------------------------------------------------

    numeric_columns = [
        "home_score",
        "away_score",
        "home_pens",
        "away_pens",
    ]

    for column in numeric_columns:

        if column in df.columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce",
            )

    # -----------------------------------------------------
    # 문자열 공백 제거
    # -----------------------------------------------------

    df["round"] = (
        df["round"]
        .astype(str)
        .str.strip()
    )

    df["home_team"] = (
        df["home_team"]
        .astype(str)
        .str.strip()
    )

    df["away_team"] = (
        df["away_team"]
        .astype(str)
        .str.strip()
    )

    return df

# =========================================================
# 경기 승리팀 계산
# =========================================================

def get_match_winner(row):

    home_team = row["home_team"]
    away_team = row["away_team"]

    home_score = row["home_score"]
    away_score = row["away_score"]

    # 점수가 없는 경기
    if (
        pd.isna(home_score)
        or
        pd.isna(away_score)
    ):
        return None

    # 홈팀 승리
    if home_score > away_score:
        return home_team


    # 원정팀 승리
    if away_score > home_score:
        return away_team

    # -----------------------------------------------------
    # 동점일 경우 승부차기 확인
    # -----------------------------------------------------

    home_pens = row.get(
        "home_pens"
    )

    away_pens = row.get(
        "away_pens"
    )

    if (
        pd.notna(home_pens)
        and
        pd.notna(away_pens)
    ):

        if home_pens > away_pens:
            return home_team

        if away_pens > home_pens:
            return away_team

    return None

# =========================================================
# 경기 패배팀 계산
# =========================================================

def get_match_loser(row):

    winner = get_match_winner(
        row
    )

    if winner is None:
        return None


    if winner == row["home_team"]:
        return row["away_team"]


    return row["home_team"]

# =========================================================
# 전체 팀 통계 계산
# =========================================================

def calculate_team_stats(matches_df):

    stats = {}

    # -----------------------------------------------------
    # 팀 최초 생성
    # -----------------------------------------------------

    def ensure_team(team_name):

        if team_name not in stats:

            stats[team_name] = {
                "team": team_name,
                "played": 0,
                "wins": 0,
                "draws": 0,
                "losses": 0,
                "goals_for": 0,
                "goals_against": 0,
                "points": 0,
            }

    # -----------------------------------------------------
    # 모든 경기 반복
    # -----------------------------------------------------

    for _, row in matches_df.iterrows():

        home_team = row["home_team"]
        away_team = row["away_team"]

        home_score = row["home_score"]
        away_score = row["away_score"]

        if (
            pd.isna(home_score)
            or
            pd.isna(away_score)
        ):
            continue

        home_score = int(
            home_score
        )

        away_score = int(
            away_score
        )

        ensure_team(
            home_team
        )

        ensure_team(
            away_team
        )

        # -------------------------------------------------
        # 경기수
        # -------------------------------------------------

        stats[home_team]["played"] += 1
        stats[away_team]["played"] += 1

        # -------------------------------------------------
        # 득점 / 실점
        # -------------------------------------------------

        stats[home_team][
            "goals_for"
        ] += home_score

        stats[home_team][
            "goals_against"
        ] += away_score


        stats[away_team][
            "goals_for"
        ] += away_score

        stats[away_team][
            "goals_against"
        ] += home_score

        # -------------------------------------------------
        # 승 / 무 / 패 / 승점
        # -------------------------------------------------

        if home_score > away_score:

            stats[home_team][
                "wins"
            ] += 1

            stats[home_team][
                "points"
            ] += 3

            stats[away_team][
                "losses"
            ] += 1

        elif away_score > home_score:

            stats[away_team][
                "wins"
            ] += 1

            stats[away_team][
                "points"
            ] += 3

            stats[home_team][
                "losses"
            ] += 1

        else:

            # 승부차기 여부와 상관없이
            # 경기 점수가 동점이면 통계상 무승부

            stats[home_team][
                "draws"
            ] += 1

            stats[away_team][
                "draws"
            ] += 1


            stats[home_team][
                "points"
            ] += 1

            stats[away_team][
                "points"
            ] += 1

    # -----------------------------------------------------
    # DataFrame으로 변환
    # -----------------------------------------------------

    team_stats = pd.DataFrame(
        stats.values()
    )

    # -----------------------------------------------------
    # 득실차
    # -----------------------------------------------------

    team_stats[
        "goal_diff"
    ] = (
        team_stats["goals_for"]
        -
        team_stats["goals_against"]
    )

    return team_stats

# =========================================================
# 특정 라운드 탈락팀
# =========================================================

def get_round_losers(
    matches_df,
    round_name,
):
    round_df = matches_df[
        matches_df["round"]
        == round_name
    ]

    losers = []

    for _, row in round_df.iterrows():

        loser = get_match_loser(
            row
        )


        if loser is not None:

            losers.append(
                loser
            )


    return losers

# =========================================================
# 같은 라운드 탈락팀 정렬
# =========================================================

def sort_same_round(
    team_list,
    team_stats,
):

    filtered = team_stats[
        team_stats["team"].isin(
            team_list
        )
    ].copy()


    filtered = filtered.sort_values(
        by=[
            "points",
            "goal_diff",
            "goals_for",
            "team",
        ],
        ascending=[
            False,
            False,
            False,
            True,
        ],
    )

    return (
        filtered["team"]
        .tolist()
    )

# =========================================================
# 최종 순위 계산
# =========================================================

def build_final_ranking(
    matches_df,
):

    team_stats = calculate_team_stats(
        matches_df
    )

    # =====================================================
    # 1위 / 2위
    # 결승전
    # =====================================================

    final_df = matches_df[
        matches_df["round"]
        == "결승"
    ]

    if final_df.empty:

        raise ValueError(
            "결승 경기 데이터를 찾을 수 없습니다."
        )


    final_match = (
        final_df.iloc[0]
    )

    champion = get_match_winner(
        final_match
    )

    runner_up = get_match_loser(
        final_match
    )

    if (
        champion is None
        or
        runner_up is None
    ):

        raise ValueError(
            "결승전 승패를 계산할 수 없습니다."
        )

    # =====================================================
    # 3위 / 4위
    # =====================================================

    third_place_df = matches_df[
        matches_df["round"]
        == "3·4위전"
    ]

    if third_place_df.empty:

        raise ValueError(
            "3·4위전 경기 데이터를 찾을 수 없습니다."
        )

    third_match = (
        third_place_df.iloc[0]
    )

    third_place = get_match_winner(
        third_match
    )

    fourth_place = get_match_loser(
        third_match
    )

    if (
        third_place is None
        or
        fourth_place is None
    ):

        raise ValueError(
            "3·4위전 승패를 계산할 수 없습니다."
        )

    # =====================================================
    # 8강 탈락팀
    # =====================================================

    quarterfinal_losers = (
        get_round_losers(
            matches_df,
            "8강",
        )
    )

    quarterfinal_losers = (
        sort_same_round(
            quarterfinal_losers,
            team_stats,
        )
    )

    # =====================================================
    # 16강 탈락팀
    # =====================================================

    round16_losers = (
        get_round_losers(
            matches_df,
            "16강",
        )
    )

    round16_losers = (
        sort_same_round(
            round16_losers,
            team_stats,
        )
    )

    # =====================================================
    # 32강 탈락팀
    # =====================================================

    round32_losers = (
        get_round_losers(
            matches_df,
            "32강",
        )
    )

    round32_losers = (
        sort_same_round(
            round32_losers,
            team_stats,
        )
    )

    # =====================================================
    # 조별리그 탈락팀 찾기
    # =====================================================

    all_teams = set(
        matches_df[
            "home_team"
        ].tolist()
        +
        matches_df[
            "away_team"
        ].tolist()
    )

    round32_df = matches_df[
        matches_df["round"]
        == "32강"
    ]

    round32_teams = set(
        round32_df[
            "home_team"
        ].tolist()
        +
        round32_df[
            "away_team"
        ].tolist()
    )

    group_stage_losers = list(
        all_teams
        -
        round32_teams
    )


    group_stage_losers = (
        sort_same_round(
            group_stage_losers,
            team_stats,
        )
    )

    # =====================================================
    # 최종 순서 결합
    # =====================================================

    ranking_order = [
        champion,
        runner_up,
        third_place,
        fourth_place,
    ]


    ranking_order += (
        quarterfinal_losers
    )

    ranking_order += (
        round16_losers
    )

    ranking_order += (
        round32_losers
    )

    ranking_order += (
        group_stage_losers
    )

    # -----------------------------------------------------
    # 혹시 중복된 팀이 있으면 제거
    # 순서는 그대로 유지
    # -----------------------------------------------------

    ranking_order = list(
        dict.fromkeys(
            ranking_order
        )
    )

    # -----------------------------------------------------
    # 순위 DataFrame 생성
    # -----------------------------------------------------

    ranking_df = pd.DataFrame(
        {
            "team": ranking_order
        }
    )

    ranking_df["rank"] = range(
        1,
        len(ranking_df) + 1,
    )

    # -----------------------------------------------------
    # 통계 붙이기
    # -----------------------------------------------------

    ranking_df = (
        ranking_df
        .merge(
            team_stats,
            on="team",
            how="left",
        )
    )

    return ranking_df

# =========================================================
# 순위에 따른 진출 단계
# =========================================================

def get_stage_name(rank):

    if rank == 1:
        return "우승"

    if rank == 2:
        return "준우승"

    if rank == 3:
        return "3위"

    if rank == 4:
        return "4위"

    if rank <= 8:
        return "8강"

    if rank <= 16:
        return "16강"

    if rank <= 32:
        return "32강"

    return "조별리그"

# =========================================================
# 순위 아이콘
# =========================================================

def get_rank_icon(rank):

    if rank == 1:
        return "🏆"

    if rank == 2:
        return "🥈"

    if rank == 3:
        return "🥉"

    return "⚽"

# =========================================================
# TAB 1
# 월드컵 최종 순위
# =========================================================

with tab1:

    st.subheader(
        "🏆 월드컵 최종 성적"
    )


    st.caption(
        "결승과 토너먼트 진출 단계를 기준으로 "
        "월드컵 종합 순위를 계산합니다."
    )

    try:

        # -------------------------------------------------
        # 경기 데이터 읽기
        # -------------------------------------------------

        matches_df = load_matches()


        # -------------------------------------------------
        # 순위 계산
        # -------------------------------------------------

        ranking_df = (
            build_final_ranking(
                matches_df
            )
        )

        if ranking_df.empty:

            st.warning(
                "순위 데이터가 없습니다."
            )

            st.stop()

        # =================================================
        # TOP 3
        # =================================================

        first = (
            ranking_df.iloc[0]
        )

        second = (
            ranking_df.iloc[1]
        )

        third = (
            ranking_df.iloc[2]
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        with col1:

            st.metric(
                "🏆 우승",
                first["team"],
            )

        with col2:

            st.metric(
                "🥈 준우승",
                second["team"],
            )

        with col3:

            st.metric(
                "🥉 3위",
                third["team"],
            )

        st.divider()

        # =================================================
        # 상위 15개 국가만 표시
        # =================================================

        st.subheader(
            "🏟️ 상위 15개 국가 순위"
        )

        st.caption(
            "상위 15개 국가만 랭킹 보드에 표시하며, "
            "전체 참가국은 하단의 전체 순위표에서 확인할 수 있습니다."
        )

        # -------------------------------------------------
        # 1위 ~ 15위
        # -------------------------------------------------

        top15_df = (
            ranking_df
            .head(15)
        )

        total_teams = len(
            ranking_df
        )

        # -------------------------------------------------
        # 가운데 정렬
        #
        # 왼쪽 15%
        # 가운데 70%
        # 오른쪽 15%
        # -------------------------------------------------

        left_space, center, right_space = (
            st.columns(
                [
                    1.5,
                    7,
                    1.5,
                ]
            )
        )

        with center:

            for _, row in top15_df.iterrows():

                rank = int(
                    row["rank"]
                )

                team = row["team"]

                points = int(
                    row["points"]
                )

                goal_diff = int(
                    row["goal_diff"]
                )

                goals_for = int(
                    row["goals_for"]
                )

                goals_against = int(
                    row["goals_against"]
                )

                stage = (
                    get_stage_name(
                        rank
                    )
                )

                icon = (
                    get_rank_icon(
                        rank
                    )
                )

                # -----------------------------------------
                # 득실차 + 기호
                # -----------------------------------------

                if goal_diff > 0:

                    goal_diff_text = (
                        f"+{goal_diff}"
                    )

                else:

                    goal_diff_text = (
                        str(goal_diff)
                    )

                # -----------------------------------------
                # 막대 길이 계산
                #
                # 1위가 가장 길고
                # 순위가 낮아질수록 줄어듦
                # -----------------------------------------

                progress_value = int(
                    100
                    -
                    (
                        (rank - 1)
                        /
                        max(
                            total_teams - 1,
                            1,
                        )
                        * 80
                    )
                )

                # -----------------------------------------
                # 순위 / 팀 이름
                # -----------------------------------------

                st.markdown(
                    f"### {icon} {rank}위 · {team}"
                )

                # -----------------------------------------
                # 순위 막대
                # -----------------------------------------

                st.progress(
                    progress_value,
                    text=(
                        f"{stage} · "
                        f"승점 {points}점 · "
                        f"득실차 {goal_diff_text}"
                    ),
                )

                # -----------------------------------------
                # 득점 / 실점 / 득실차
                # -----------------------------------------

                stat1, stat2, stat3 = (
                    st.columns(3)
                )

                with stat1:

                    st.caption(
                        f"⚽ 득점 {goals_for}"
                    )

                with stat2:

                    st.caption(
                        f"🥅 실점 {goals_against}"
                    )

                with stat3:

                    st.caption(
                        f"📊 득실차 {goal_diff_text}"
                    )

                st.divider()

        # =================================================
        # 전체 순위표
        # =================================================

        st.subheader(
            "📋 전체 참가국 순위표"
        )

        with st.expander(
            "전체 순위표 보기"
        ):

            display_df = ranking_df[
                [
                    "rank",
                    "team",
                    "played",
                    "wins",
                    "draws",
                    "losses",
                    "goals_for",
                    "goals_against",
                    "goal_diff",
                    "points",
                ]
            ].copy()

            # ---------------------------------------------
            # 한글 컬럼명
            # ---------------------------------------------

            display_df.columns = [
                "순위",
                "국가",
                "경기",
                "승",
                "무",
                "패",
                "득점",
                "실점",
                "득실차",
                "승점",
            ]

            st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
            )

        st.info(
            "1~4위는 결승 및 3·4위전 실제 결과를 기준으로 합니다. "
            "5위 이하는 같은 토너먼트 단계에서 탈락한 국가끼리 "
            "승점 → 득실차 → 득점 순으로 정렬한 프로젝트 종합 순위입니다."
        )

    except Exception as e:

        st.error(
            f"순위 계산 중 오류가 발생했습니다: {e}"
        )

# =========================================================
# TAB 2
# 선수 득점 통계
# =========================================================

with tab2:

    st.subheader(
        "⚽ 득점 상위 선수"
    )

    limit = st.slider(
        "표시할 선수 수",
        min_value=5,
        max_value=30,
        value=10,
    )

    if st.button(
        "득점 통계 불러오기",
        type="primary",
        use_container_width=True,
    ):

        try:

            data = (
                get_top_scorers(
                    limit=limit
                )
            )

            df = pd.DataFrame(
                data
            )

            if df.empty:

                st.warning(
                    "득점 통계 데이터가 없습니다."
                )

            else:

                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True,
                )

                # -----------------------------------------
                # 90분당 득점 컬럼이 있을 경우 그래프
                # -----------------------------------------

                if (
                    "player"
                    in df.columns
                    and
                    "goals_per_90"
                    in df.columns
                ):

                    chart_df = (
                        df[
                            [
                                "player",
                                "goals_per_90",
                            ]
                        ]
                        .set_index(
                            "player"
                        )
                    )

                    st.bar_chart(
                        chart_df
                    )

        except Exception as e:

            st.error(
                "선수 통계를 불러오는 중 "
                f"오류가 발생했습니다: {e}"
            )