# ==============================================================
# routers/stats.py
# - pandas로 SQL 결과를 집계해서 응답하는 API
# - models.py에는 핵심 컬럼만 매핑해뒀지만, 여기서는 pandas.read_sql()로
#   테이블 전체 컬럼을 직접 읽어와서 자유롭게 계산해본다.
# ==============================================================
import pandas as pd
from fastapi import APIRouter, Query
from starlette import status

from database.db_connection import engine

router = APIRouter(tags=['Stats'])


# GET /stats/top-scorers --> 90분당 득점 상위 선수 (pandas 계산)
@router.get('/stats/top-scorers', status_code=status.HTTP_200_OK)
def top_scorers_handler(
    min_minutes: int = Query(180, description='최소 출전 시간(분) 필터'),
    limit: int = Query(10, ge=1, le=50),
):
    df = pd.read_sql('SELECT player, team, position, minutes, goals, assists FROM players', engine)
    df = df[df['minutes'] >= min_minutes].copy()
    df['goals_per90'] = (df['goals'] / (df['minutes'] / 90)).round(2)
    df = df.sort_values('goals_per90', ascending=False).head(limit)
    return df.to_dict(orient='records')


# GET /stats/team-goal-diff --> 팀별 득실차/승점 순위표 (pandas 계산)
@router.get('/stats/team-goal-diff', status_code=status.HTTP_200_OK)
def team_goal_diff_handler():
    df = pd.read_sql(
        'SELECT home_team, away_team, home_score, away_score FROM matches '
        'WHERE home_score IS NOT NULL AND away_score IS NOT NULL',
        engine,
    )

    home = df.rename(columns={
        'home_team': 'team', 'away_team': 'opponent',
        'home_score': 'goals_for', 'away_score': 'goals_against',
    })[['team', 'opponent', 'goals_for', 'goals_against']]

    away = df.rename(columns={
        'away_team': 'team', 'home_team': 'opponent',
        'away_score': 'goals_for', 'home_score': 'goals_against',
    })[['team', 'opponent', 'goals_for', 'goals_against']]

    long_df = pd.concat([home, away], ignore_index=True)

    def result_points(row):
        if row['goals_for'] > row['goals_against']:
            return 3
        if row['goals_for'] == row['goals_against']:
            return 1
        return 0

    long_df['points'] = long_df.apply(result_points, axis=1)

    summary = (
        long_df.groupby('team')
        .agg(
            played=('team', 'count'),
            goals_for=('goals_for', 'sum'),
            goals_against=('goals_against', 'sum'),
            points=('points', 'sum'),
        )
        .reset_index()
    )
    summary['goal_diff'] = summary['goals_for'] - summary['goals_against']
    summary = summary.sort_values(['points', 'goal_diff'], ascending=False)
    return summary.to_dict(orient='records')
