from pydantic import BaseModel

# 선수 생성 요청 모델
class PlayerCreateRequest(BaseModel):
    player: str
    team: str
    position: str
    team_country: str | None = None
    age: int | None = None
    club: str | None = None
    games: int | None = 0
    goals: float | None = 0
    assists: float | None = 0


# 선수 수정 요청 모델
# 전 필드를 Optional로 둔 이유 -> TROUBLESHOOTING.md 1번 참고
# (PUT으로 필드 1개만 보내도 나머지가 required라서 422가 계속 났었음)
class PlayerUpdateRequest(BaseModel):
    player: str | None = None
    team: str | None = None
    team_country: str | None = None
    position: str | None = None
    age: int | None = None
    club: str | None = None
    games: int | None = None
    goals: float | None = None
    assists: float | None = None


# 로그인 요청 모델 (JWT 발급용, 회원 테이블 없이 .env 고정 계정만 사용)
class LoginRequest(BaseModel):
    username: str
    password: str
