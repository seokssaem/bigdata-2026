from datetime import date, time
from pydantic import BaseModel, ConfigDict


# 선수 응답 모델
class PlayerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)  # ORM 객체를 그대로 응답으로 변환 가능하게 함

    id: int
    player: str | None
    team: str | None
    team_country: str | None
    position: str | None
    age: int | None
    club: str | None
    games: int | None
    goals: float | None
    assists: float | None


# 경기 응답 모델
class MatchResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    round: str | None
    date: date | None
    start_time: time | None
    home_team: str | None
    away_team: str | None
    score: str | None
    venue: str | None
    referee: str | None
    home_manager: str | None
    away_manager: str | None
    attendance: int | None


# 팀 응답 모델
class TeamResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    team: str | None
    team_country: str | None
    players_used: int | None
    avg_age: float | None
    possession: float | None
    games: int | None
    goals: int | None
    assists: int | None
    goals_against: int | None


# 로그인 응답 모델
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = 'bearer'
