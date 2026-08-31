--  2026 FIFA 월드컵 데이터 스키마 (자동 생성)
-- players / matches / teams 3개 테이블. 텍스트 값은 한국어로 정리됨 (position 제외)

DROP TABLE IF EXISTS players CASCADE;
CREATE TABLE players (
    "players_id" SERIAL PRIMARY KEY,
    "player" TEXT,
    "team" TEXT,
    "team_country" TEXT,
    "position" TEXT,
    "age" INTEGER,
    "birth_year" INTEGER,
    "club" TEXT,
    "games" INTEGER,
    "games_starts" INTEGER,
    "minutes" NUMERIC,
    "minutes_90s" NUMERIC,
    "goals" NUMERIC,
    "assists" NUMERIC,
    "goals_assists" NUMERIC,
    "goals_pens" NUMERIC,
    "pens_made" NUMERIC,
    "pens_att" NUMERIC,
    "cards_yellow" NUMERIC,
    "cards_red" NUMERIC,
    "goals_per90" NUMERIC,
    "assists_per90" NUMERIC,
    "goals_assists_per90" NUMERIC,
    "goals_pens_per90" NUMERIC,
    "goals_assists_pens_per90" NUMERIC,
    "shots" NUMERIC,
    "shots_on_target" NUMERIC,
    "shots_on_target_pct" NUMERIC,
    "shots_per90" NUMERIC,
    "shots_on_target_per90" NUMERIC,
    "goals_per_shot" NUMERIC,
    "goals_per_shot_on_target" NUMERIC,
    "minutes_per_game" NUMERIC,
    "minutes_pct" NUMERIC,
    "minutes_per_start" NUMERIC,
    "games_complete" INTEGER,
    "games_subs" INTEGER,
    "minutes_per_sub" NUMERIC,
    "unused_subs" INTEGER,
    "points_per_game" NUMERIC,
    "on_goals_for" NUMERIC,
    "on_goals_against" NUMERIC,
    "plus_minus" NUMERIC,
    "plus_minus_per90" NUMERIC,
    "plus_minus_wowy" NUMERIC,
    "cards_yellow_red" NUMERIC,
    "fouls" NUMERIC,
    "fouled" NUMERIC,
    "offsides" NUMERIC,
    "crosses" NUMERIC,
    "interceptions" NUMERIC,
    "tackles_won" NUMERIC,
    "pens_won" TEXT,
    "pens_conceded" TEXT,
    "own_goals" NUMERIC,
    "gk_games" NUMERIC,
    "gk_games_starts" NUMERIC,
    "gk_minutes" NUMERIC,
    "gk_goals_against" NUMERIC,
    "gk_goals_against_per90" NUMERIC,
    "gk_shots_on_target_against" NUMERIC,
    "gk_saves" NUMERIC,
    "gk_save_pct" NUMERIC,
    "gk_wins" NUMERIC,
    "gk_ties" NUMERIC,
    "gk_losses" NUMERIC,
    "gk_clean_sheets" NUMERIC,
    "gk_clean_sheets_pct" NUMERIC,
    "gk_pens_att" NUMERIC,
    "gk_pens_allowed" NUMERIC,
    "gk_pens_saved" NUMERIC,
    "gk_pens_missed" NUMERIC,
    "gk_pens_save_pct" NUMERIC
);

COMMENT ON COLUMN players."player" IS '선수 이름';
COMMENT ON COLUMN players."team" IS '소속 국가대표팀(팀명, 표기 축약형 가능)';
COMMENT ON COLUMN players."team_country" IS '소속 국가(전체 정식 국가명)';
COMMENT ON COLUMN players."position" IS '포지션 (GK 골키퍼, DF 수비수, MF 미드필더, FW 공격수)';
COMMENT ON COLUMN players."age" IS '대회 기준 나이';
COMMENT ON COLUMN players."birth_year" IS '출생 연도';
COMMENT ON COLUMN players."club" IS '소속 클럽(대회 시점 기준, 없으면 NULL)';
COMMENT ON COLUMN players."games" IS '출전 경기 수';
COMMENT ON COLUMN players."games_starts" IS '선발 출전 수';
COMMENT ON COLUMN players."minutes" IS '총 출전 시간(분)';
COMMENT ON COLUMN players."minutes_90s" IS '90분 환산 출전 횟수(minutes/90)';
COMMENT ON COLUMN players."goals" IS '득점 수';
COMMENT ON COLUMN players."assists" IS '도움 수';
COMMENT ON COLUMN players."goals_assists" IS '득점+도움 합계';
COMMENT ON COLUMN players."goals_pens" IS '페널티킥 제외 득점 수';
COMMENT ON COLUMN players."pens_made" IS '페널티킥 성공 수';
COMMENT ON COLUMN players."pens_att" IS '페널티킥 시도 수';
COMMENT ON COLUMN players."cards_yellow" IS '경고(옐로카드) 수';
COMMENT ON COLUMN players."cards_red" IS '퇴장(레드카드) 수';
COMMENT ON COLUMN players."goals_per90" IS '90분당 득점';
COMMENT ON COLUMN players."assists_per90" IS '90분당 도움';
COMMENT ON COLUMN players."goals_assists_per90" IS '90분당 득점+도움';
COMMENT ON COLUMN players."goals_pens_per90" IS '90분당 비-PK 득점';
COMMENT ON COLUMN players."goals_assists_pens_per90" IS '90분당 비-PK 득점+도움';
COMMENT ON COLUMN players."shots" IS '슈팅 수';
COMMENT ON COLUMN players."shots_on_target" IS '유효슈팅 수';
COMMENT ON COLUMN players."shots_on_target_pct" IS '유효슈팅 비율(%)';
COMMENT ON COLUMN players."shots_per90" IS '90분당 슈팅 수';
COMMENT ON COLUMN players."shots_on_target_per90" IS '90분당 유효슈팅 수';
COMMENT ON COLUMN players."goals_per_shot" IS '슈팅당 득점(득점/슈팅)';
COMMENT ON COLUMN players."goals_per_shot_on_target" IS '유효슈팅당 득점';
COMMENT ON COLUMN players."minutes_per_game" IS '경기당 평균 출전 시간(분)';
COMMENT ON COLUMN players."minutes_pct" IS '팀 전체 가용 시간 대비 출전 비율(%)';
COMMENT ON COLUMN players."minutes_per_start" IS '선발 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN players."games_complete" IS '풀타임(90분 전체) 출전 경기 수';
COMMENT ON COLUMN players."games_subs" IS '교체로 출전한 경기 수';
COMMENT ON COLUMN players."minutes_per_sub" IS '교체 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN players."unused_subs" IS '교체 명단에만 포함되고 출전하지 못한 횟수';
COMMENT ON COLUMN players."points_per_game" IS '출전 경기당 팀 승점 평균';
COMMENT ON COLUMN players."on_goals_for" IS '해당 선수가 뛰는 동안 팀이 넣은 골 수';
COMMENT ON COLUMN players."on_goals_against" IS '해당 선수가 뛰는 동안 팀이 내준 골 수';
COMMENT ON COLUMN players."plus_minus" IS '온-필드 득실차(on_goals_for - on_goals_against)';
COMMENT ON COLUMN players."plus_minus_per90" IS '90분당 온-필드 득실차';
COMMENT ON COLUMN players."plus_minus_wowy" IS '출전 유무에 따른 팀 득실차 비교 지표(With Or Without You)';
COMMENT ON COLUMN players."cards_yellow_red" IS '경고 누적 퇴장(옐로 2장) 수';
COMMENT ON COLUMN players."fouls" IS '범한 파울 수';
COMMENT ON COLUMN players."fouled" IS '당한 파울 수';
COMMENT ON COLUMN players."offsides" IS '오프사이드 수';
COMMENT ON COLUMN players."crosses" IS '크로스 시도 수';
COMMENT ON COLUMN players."interceptions" IS '인터셉트(가로채기) 수';
COMMENT ON COLUMN players."tackles_won" IS '성공한 태클 수';
COMMENT ON COLUMN players."pens_won" IS '얻어낸 페널티킥 수';
COMMENT ON COLUMN players."pens_conceded" IS '내준 페널티킥 수';
COMMENT ON COLUMN players."own_goals" IS '자책골 수';
COMMENT ON COLUMN players."gk_games" IS '골키퍼로 출전한 경기 수';
COMMENT ON COLUMN players."gk_games_starts" IS '골키퍼로 선발 출전한 경기 수';
COMMENT ON COLUMN players."gk_minutes" IS '골키퍼로 출전한 시간(분)';
COMMENT ON COLUMN players."gk_goals_against" IS '실점 수(골키퍼 기준)';
COMMENT ON COLUMN players."gk_goals_against_per90" IS '90분당 실점';
COMMENT ON COLUMN players."gk_shots_on_target_against" IS '상대의 유효슈팅 수(골키퍼 기준)';
COMMENT ON COLUMN players."gk_saves" IS '선방 수';
COMMENT ON COLUMN players."gk_save_pct" IS '선방률(%)';
COMMENT ON COLUMN players."gk_wins" IS '골키퍼로 출전해 승리한 경기 수';
COMMENT ON COLUMN players."gk_ties" IS '골키퍼로 출전해 무승부한 경기 수';
COMMENT ON COLUMN players."gk_losses" IS '골키퍼로 출전해 패배한 경기 수';
COMMENT ON COLUMN players."gk_clean_sheets" IS '무실점 경기 수(클린시트)';
COMMENT ON COLUMN players."gk_clean_sheets_pct" IS '무실점 경기 비율(%)';
COMMENT ON COLUMN players."gk_pens_att" IS '상대의 페널티킥 시도 수(대응)';
COMMENT ON COLUMN players."gk_pens_allowed" IS '페널티킥 실점 허용 수';
COMMENT ON COLUMN players."gk_pens_saved" IS '페널티킥 선방 수';
COMMENT ON COLUMN players."gk_pens_missed" IS '상대가 실축한 페널티킥 수';
COMMENT ON COLUMN players."gk_pens_save_pct" IS '페널티킥 선방률(%)';

DROP TABLE IF EXISTS matches CASCADE;
CREATE TABLE matches (
    "matches_id" SERIAL PRIMARY KEY,
    "round" TEXT,
    "gameweek" INTEGER,
    "dayofweek" TEXT,
    "date" DATE,
    "start_time" TIME,
    "home_team" TEXT,
    "away_team" TEXT,
    "score" TEXT,
    "home_score" NUMERIC,
    "away_score" NUMERIC,
    "home_pens" INTEGER,
    "away_pens" INTEGER,
    "went_to_penalties" BOOLEAN,
    "attendance" INTEGER,
    "venue" TEXT,
    "referee" TEXT,
    "home_formation" TEXT,
    "away_formation" TEXT,
    "home_manager" TEXT,
    "away_manager" TEXT,
    "home_captain" TEXT,
    "away_captain" TEXT,
    "home_possession" INTEGER,
    "away_possession" INTEGER,
    "home_sot" INTEGER,
    "away_sot" INTEGER,
    "home_total_shots" INTEGER,
    "away_total_shots" INTEGER,
    "home_saves" INTEGER,
    "away_saves" INTEGER,
    "home_cards_yellow" INTEGER,
    "away_cards_yellow" INTEGER,
    "home_cards_red" INTEGER,
    "away_cards_red" INTEGER,
    "home_fouls" INTEGER,
    "away_fouls" INTEGER,
    "home_corners" INTEGER,
    "away_corners" INTEGER,
    "home_crosses" INTEGER,
    "away_crosses" INTEGER,
    "home_interceptions" INTEGER,
    "away_interceptions" INTEGER,
    "home_offsides" INTEGER,
    "away_offsides" INTEGER,
    "notes" TEXT
);

COMMENT ON COLUMN matches."round" IS '라운드/스테이지 (조별리그, 16강 등)';
COMMENT ON COLUMN matches."gameweek" IS '조별리그 라운드 번호(조별리그 1~3라운드, 토너먼트는 공란)';
COMMENT ON COLUMN matches."dayofweek" IS '요일';
COMMENT ON COLUMN matches."date" IS '경기 날짜';
COMMENT ON COLUMN matches."start_time" IS '경기 시작 시각(현지시각)';
COMMENT ON COLUMN matches."home_team" IS '홈팀(대회 특성상 편의상 지정된 팀, 중립경기 다수)';
COMMENT ON COLUMN matches."away_team" IS '원정팀';
COMMENT ON COLUMN matches."score" IS '최종 스코어 (정규시간+연장 기준, ''홈-원정'' 형식)';
COMMENT ON COLUMN matches."home_score" IS '홈팀 득점 수(정규시간+연장 기준)';
COMMENT ON COLUMN matches."away_score" IS '원정팀 득점 수(정규시간+연장 기준)';
COMMENT ON COLUMN matches."home_pens" IS '승부차기 홈팀 득점 수(승부차기가 없으면 NULL)';
COMMENT ON COLUMN matches."away_pens" IS '승부차기 원정팀 득점 수(승부차기가 없으면 NULL)';
COMMENT ON COLUMN matches."went_to_penalties" IS '승부차기 진행 여부(true/false)';
COMMENT ON COLUMN matches."attendance" IS '관중 수';
COMMENT ON COLUMN matches."venue" IS '경기장';
COMMENT ON COLUMN matches."referee" IS '주심';
COMMENT ON COLUMN matches."home_formation" IS '홈팀 포메이션';
COMMENT ON COLUMN matches."away_formation" IS '원정팀 포메이션';
COMMENT ON COLUMN matches."home_manager" IS '홈팀 감독';
COMMENT ON COLUMN matches."away_manager" IS '원정팀 감독';
COMMENT ON COLUMN matches."home_captain" IS '홈팀 주장';
COMMENT ON COLUMN matches."away_captain" IS '원정팀 주장';
COMMENT ON COLUMN matches."home_possession" IS '홈팀 점유율(%)';
COMMENT ON COLUMN matches."away_possession" IS '원정팀 점유율(%)';
COMMENT ON COLUMN matches."home_sot" IS '홈팀 유효슈팅 수';
COMMENT ON COLUMN matches."away_sot" IS '원정팀 유효슈팅 수';
COMMENT ON COLUMN matches."home_total_shots" IS '홈팀 총 슈팅 수';
COMMENT ON COLUMN matches."away_total_shots" IS '원정팀 총 슈팅 수';
COMMENT ON COLUMN matches."home_saves" IS '홈팀 골키퍼 선방 수';
COMMENT ON COLUMN matches."away_saves" IS '원정팀 골키퍼 선방 수';
COMMENT ON COLUMN matches."home_cards_yellow" IS '홈팀 경고 수';
COMMENT ON COLUMN matches."away_cards_yellow" IS '원정팀 경고 수';
COMMENT ON COLUMN matches."home_cards_red" IS '홈팀 퇴장 수';
COMMENT ON COLUMN matches."away_cards_red" IS '원정팀 퇴장 수';
COMMENT ON COLUMN matches."home_fouls" IS '홈팀 파울 수';
COMMENT ON COLUMN matches."away_fouls" IS '원정팀 파울 수';
COMMENT ON COLUMN matches."home_corners" IS '홈팀 코너킥 수';
COMMENT ON COLUMN matches."away_corners" IS '원정팀 코너킥 수';
COMMENT ON COLUMN matches."home_crosses" IS '홈팀 크로스 수';
COMMENT ON COLUMN matches."away_crosses" IS '원정팀 크로스 수';
COMMENT ON COLUMN matches."home_interceptions" IS '홈팀 인터셉트 수';
COMMENT ON COLUMN matches."away_interceptions" IS '원정팀 인터셉트 수';
COMMENT ON COLUMN matches."home_offsides" IS '홈팀 오프사이드 수';
COMMENT ON COLUMN matches."away_offsides" IS '원정팀 오프사이드 수';
COMMENT ON COLUMN matches."notes" IS '비고(연장전, 승부차기 승리팀 등 특이사항)';

DROP TABLE IF EXISTS teams CASCADE;
CREATE TABLE teams (
    "teams_id" SERIAL PRIMARY KEY,
    "team" TEXT,
    "team_country" TEXT,
    "players_used" INTEGER,
    "avg_age" NUMERIC,
    "possession" NUMERIC,
    "games" INTEGER,
    "games_starts" INTEGER,
    "minutes" INTEGER,
    "minutes_90s" NUMERIC,
    "goals" INTEGER,
    "assists" INTEGER,
    "goals_assists" INTEGER,
    "goals_pens" INTEGER,
    "pens_made" INTEGER,
    "pens_att" INTEGER,
    "cards_yellow" INTEGER,
    "cards_red" INTEGER,
    "goals_per90" NUMERIC,
    "assists_per90" NUMERIC,
    "goals_assists_per90" NUMERIC,
    "goals_pens_per90" NUMERIC,
    "goals_assists_pens_per90" NUMERIC,
    "players_used_against" INTEGER,
    "avg_age_against" NUMERIC,
    "possession_against" NUMERIC,
    "games_against" INTEGER,
    "games_starts_against" INTEGER,
    "minutes_against" INTEGER,
    "minutes_90s_against" NUMERIC,
    "goals_against" INTEGER,
    "assists_against" INTEGER,
    "goals_assists_against" INTEGER,
    "goals_pens_against" INTEGER,
    "pens_made_against" INTEGER,
    "pens_att_against" INTEGER,
    "cards_yellow_against" INTEGER,
    "cards_red_against" INTEGER,
    "goals_per90_against" NUMERIC,
    "assists_per90_against" NUMERIC,
    "goals_assists_per90_against" NUMERIC,
    "goals_pens_per90_against" NUMERIC,
    "goals_assists_pens_per90_against" NUMERIC,
    "shots" INTEGER,
    "shots_on_target" INTEGER,
    "shots_on_target_pct" NUMERIC,
    "shots_per90" NUMERIC,
    "shots_on_target_per90" NUMERIC,
    "goals_per_shot" NUMERIC,
    "goals_per_shot_on_target" NUMERIC,
    "shots_against" INTEGER,
    "shots_on_target_against" INTEGER,
    "shots_on_target_pct_against" NUMERIC,
    "shots_per90_against" NUMERIC,
    "shots_on_target_per90_against" NUMERIC,
    "goals_per_shot_against" NUMERIC,
    "goals_per_shot_on_target_against" NUMERIC,
    "minutes_per_game" INTEGER,
    "minutes_pct" INTEGER,
    "minutes_per_start" INTEGER,
    "games_complete" INTEGER,
    "games_subs" INTEGER,
    "minutes_per_sub" INTEGER,
    "unused_subs" INTEGER,
    "points_per_game" NUMERIC,
    "on_goals_for" INTEGER,
    "on_goals_against" INTEGER,
    "plus_minus" INTEGER,
    "plus_minus_per90" NUMERIC,
    "minutes_per_game_against" INTEGER,
    "minutes_pct_against" INTEGER,
    "minutes_per_start_against" INTEGER,
    "games_complete_against" INTEGER,
    "games_subs_against" INTEGER,
    "minutes_per_sub_against" INTEGER,
    "unused_subs_against" INTEGER,
    "points_per_game_against" NUMERIC,
    "on_goals_for_against" INTEGER,
    "on_goals_against_against" INTEGER,
    "plus_minus_against" INTEGER,
    "plus_minus_per90_against" NUMERIC,
    "cards_yellow_red" INTEGER,
    "fouls" INTEGER,
    "fouled" INTEGER,
    "offsides" INTEGER,
    "crosses" INTEGER,
    "interceptions" INTEGER,
    "tackles_won" INTEGER,
    "pens_won" TEXT,
    "pens_conceded" TEXT,
    "own_goals" INTEGER,
    "cards_yellow_red_against" INTEGER,
    "fouls_against" INTEGER,
    "fouled_against" INTEGER,
    "offsides_against" INTEGER,
    "crosses_against" INTEGER,
    "interceptions_against" INTEGER,
    "tackles_won_against" INTEGER,
    "pens_won_against" TEXT,
    "pens_conceded_against" TEXT,
    "own_goals_against" INTEGER,
    "gk_games" INTEGER,
    "gk_games_starts" INTEGER,
    "gk_minutes" INTEGER,
    "gk_goals_against" INTEGER,
    "gk_goals_against_per90" NUMERIC,
    "gk_shots_on_target_against" INTEGER,
    "gk_saves" INTEGER,
    "gk_save_pct" NUMERIC,
    "gk_wins" INTEGER,
    "gk_ties" INTEGER,
    "gk_losses" INTEGER,
    "gk_clean_sheets" INTEGER,
    "gk_clean_sheets_pct" NUMERIC,
    "gk_pens_att" INTEGER,
    "gk_pens_allowed" INTEGER,
    "gk_pens_saved" INTEGER,
    "gk_pens_missed" INTEGER,
    "gk_pens_save_pct" NUMERIC,
    "gk_games_against" INTEGER,
    "gk_games_starts_against" INTEGER,
    "gk_minutes_against" INTEGER,
    "gk_goals_against_against" INTEGER,
    "gk_goals_against_per90_against" NUMERIC,
    "gk_shots_on_target_against_against" INTEGER,
    "gk_saves_against" INTEGER,
    "gk_save_pct_against" NUMERIC,
    "gk_wins_against" INTEGER,
    "gk_ties_against" INTEGER,
    "gk_losses_against" INTEGER,
    "gk_clean_sheets_against" INTEGER,
    "gk_clean_sheets_pct_against" NUMERIC,
    "gk_pens_att_against" INTEGER,
    "gk_pens_allowed_against" INTEGER,
    "gk_pens_saved_against" INTEGER,
    "gk_pens_missed_against" INTEGER,
    "gk_pens_save_pct_against" NUMERIC
);

COMMENT ON COLUMN teams."team" IS '소속 국가대표팀(팀명, 표기 축약형 가능)';
COMMENT ON COLUMN teams."team_country" IS '소속 국가(전체 정식 국가명)';
COMMENT ON COLUMN teams."players_used" IS '대회에서 기용된 선수 수';
COMMENT ON COLUMN teams."avg_age" IS '평균 나이';
COMMENT ON COLUMN teams."possession" IS '평균 점유율(%)';
COMMENT ON COLUMN teams."games" IS '출전 경기 수';
COMMENT ON COLUMN teams."games_starts" IS '선발 출전 수';
COMMENT ON COLUMN teams."minutes" IS '총 출전 시간(분)';
COMMENT ON COLUMN teams."minutes_90s" IS '90분 환산 출전 횟수(minutes/90)';
COMMENT ON COLUMN teams."goals" IS '득점 수';
COMMENT ON COLUMN teams."assists" IS '도움 수';
COMMENT ON COLUMN teams."goals_assists" IS '득점+도움 합계';
COMMENT ON COLUMN teams."goals_pens" IS '페널티킥 제외 득점 수';
COMMENT ON COLUMN teams."pens_made" IS '페널티킥 성공 수';
COMMENT ON COLUMN teams."pens_att" IS '페널티킥 시도 수';
COMMENT ON COLUMN teams."cards_yellow" IS '경고(옐로카드) 수';
COMMENT ON COLUMN teams."cards_red" IS '퇴장(레드카드) 수';
COMMENT ON COLUMN teams."goals_per90" IS '90분당 득점';
COMMENT ON COLUMN teams."assists_per90" IS '90분당 도움';
COMMENT ON COLUMN teams."goals_assists_per90" IS '90분당 득점+도움';
COMMENT ON COLUMN teams."goals_pens_per90" IS '90분당 비-PK 득점';
COMMENT ON COLUMN teams."goals_assists_pens_per90" IS '90분당 비-PK 득점+도움';
COMMENT ON COLUMN teams."players_used_against" IS '[상대팀 기준] 대회에서 기용된 선수 수';
COMMENT ON COLUMN teams."avg_age_against" IS '[상대팀 기준] 평균 나이';
COMMENT ON COLUMN teams."possession_against" IS '[상대팀 기준] 평균 점유율(%)';
COMMENT ON COLUMN teams."games_against" IS '[상대팀 기준] 출전 경기 수';
COMMENT ON COLUMN teams."games_starts_against" IS '[상대팀 기준] 선발 출전 수';
COMMENT ON COLUMN teams."minutes_against" IS '[상대팀 기준] 총 출전 시간(분)';
COMMENT ON COLUMN teams."minutes_90s_against" IS '[상대팀 기준] 90분 환산 출전 횟수(minutes/90)';
COMMENT ON COLUMN teams."goals_against" IS '[상대팀 기준] 득점 수';
COMMENT ON COLUMN teams."assists_against" IS '[상대팀 기준] 도움 수';
COMMENT ON COLUMN teams."goals_assists_against" IS '[상대팀 기준] 득점+도움 합계';
COMMENT ON COLUMN teams."goals_pens_against" IS '[상대팀 기준] 페널티킥 제외 득점 수';
COMMENT ON COLUMN teams."pens_made_against" IS '[상대팀 기준] 페널티킥 성공 수';
COMMENT ON COLUMN teams."pens_att_against" IS '[상대팀 기준] 페널티킥 시도 수';
COMMENT ON COLUMN teams."cards_yellow_against" IS '[상대팀 기준] 경고(옐로카드) 수';
COMMENT ON COLUMN teams."cards_red_against" IS '[상대팀 기준] 퇴장(레드카드) 수';
COMMENT ON COLUMN teams."goals_per90_against" IS '[상대팀 기준] 90분당 득점';
COMMENT ON COLUMN teams."assists_per90_against" IS '[상대팀 기준] 90분당 도움';
COMMENT ON COLUMN teams."goals_assists_per90_against" IS '[상대팀 기준] 90분당 득점+도움';
COMMENT ON COLUMN teams."goals_pens_per90_against" IS '[상대팀 기준] 90분당 비-PK 득점';
COMMENT ON COLUMN teams."goals_assists_pens_per90_against" IS '[상대팀 기준] 90분당 비-PK 득점+도움';
COMMENT ON COLUMN teams."shots" IS '슈팅 수';
COMMENT ON COLUMN teams."shots_on_target" IS '유효슈팅 수';
COMMENT ON COLUMN teams."shots_on_target_pct" IS '유효슈팅 비율(%)';
COMMENT ON COLUMN teams."shots_per90" IS '90분당 슈팅 수';
COMMENT ON COLUMN teams."shots_on_target_per90" IS '90분당 유효슈팅 수';
COMMENT ON COLUMN teams."goals_per_shot" IS '슈팅당 득점(득점/슈팅)';
COMMENT ON COLUMN teams."goals_per_shot_on_target" IS '유효슈팅당 득점';
COMMENT ON COLUMN teams."shots_against" IS '[상대팀 기준] 슈팅 수';
COMMENT ON COLUMN teams."shots_on_target_against" IS '[상대팀 기준] 유효슈팅 수';
COMMENT ON COLUMN teams."shots_on_target_pct_against" IS '[상대팀 기준] 유효슈팅 비율(%)';
COMMENT ON COLUMN teams."shots_per90_against" IS '[상대팀 기준] 90분당 슈팅 수';
COMMENT ON COLUMN teams."shots_on_target_per90_against" IS '[상대팀 기준] 90분당 유효슈팅 수';
COMMENT ON COLUMN teams."goals_per_shot_against" IS '[상대팀 기준] 슈팅당 득점(득점/슈팅)';
COMMENT ON COLUMN teams."goals_per_shot_on_target_against" IS '[상대팀 기준] 유효슈팅당 득점';
COMMENT ON COLUMN teams."minutes_per_game" IS '경기당 평균 출전 시간(분)';
COMMENT ON COLUMN teams."minutes_pct" IS '팀 전체 가용 시간 대비 출전 비율(%)';
COMMENT ON COLUMN teams."minutes_per_start" IS '선발 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN teams."games_complete" IS '풀타임(90분 전체) 출전 경기 수';
COMMENT ON COLUMN teams."games_subs" IS '교체로 출전한 경기 수';
COMMENT ON COLUMN teams."minutes_per_sub" IS '교체 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN teams."unused_subs" IS '교체 명단에만 포함되고 출전하지 못한 횟수';
COMMENT ON COLUMN teams."points_per_game" IS '출전 경기당 팀 승점 평균';
COMMENT ON COLUMN teams."on_goals_for" IS '해당 선수가 뛰는 동안 팀이 넣은 골 수';
COMMENT ON COLUMN teams."on_goals_against" IS '해당 선수가 뛰는 동안 팀이 내준 골 수';
COMMENT ON COLUMN teams."plus_minus" IS '온-필드 득실차(on_goals_for - on_goals_against)';
COMMENT ON COLUMN teams."plus_minus_per90" IS '90분당 온-필드 득실차';
COMMENT ON COLUMN teams."minutes_per_game_against" IS '[상대팀 기준] 경기당 평균 출전 시간(분)';
COMMENT ON COLUMN teams."minutes_pct_against" IS '[상대팀 기준] 팀 전체 가용 시간 대비 출전 비율(%)';
COMMENT ON COLUMN teams."minutes_per_start_against" IS '[상대팀 기준] 선발 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN teams."games_complete_against" IS '[상대팀 기준] 풀타임(90분 전체) 출전 경기 수';
COMMENT ON COLUMN teams."games_subs_against" IS '[상대팀 기준] 교체로 출전한 경기 수';
COMMENT ON COLUMN teams."minutes_per_sub_against" IS '[상대팀 기준] 교체 출전 시 평균 출전 시간(분)';
COMMENT ON COLUMN teams."unused_subs_against" IS '[상대팀 기준] 교체 명단에만 포함되고 출전하지 못한 횟수';
COMMENT ON COLUMN teams."points_per_game_against" IS '[상대팀 기준] 출전 경기당 팀 승점 평균';
COMMENT ON COLUMN teams."on_goals_for_against" IS '[상대팀 기준] 해당 선수가 뛰는 동안 팀이 넣은 골 수';
COMMENT ON COLUMN teams."on_goals_against_against" IS '[상대팀 기준] 해당 선수가 뛰는 동안 팀이 내준 골 수';
COMMENT ON COLUMN teams."plus_minus_against" IS '[상대팀 기준] 온-필드 득실차(on_goals_for - on_goals_against)';
COMMENT ON COLUMN teams."plus_minus_per90_against" IS '[상대팀 기준] 90분당 온-필드 득실차';
COMMENT ON COLUMN teams."cards_yellow_red" IS '경고 누적 퇴장(옐로 2장) 수';
COMMENT ON COLUMN teams."fouls" IS '범한 파울 수';
COMMENT ON COLUMN teams."fouled" IS '당한 파울 수';
COMMENT ON COLUMN teams."offsides" IS '오프사이드 수';
COMMENT ON COLUMN teams."crosses" IS '크로스 시도 수';
COMMENT ON COLUMN teams."interceptions" IS '인터셉트(가로채기) 수';
COMMENT ON COLUMN teams."tackles_won" IS '성공한 태클 수';
COMMENT ON COLUMN teams."pens_won" IS '얻어낸 페널티킥 수';
COMMENT ON COLUMN teams."pens_conceded" IS '내준 페널티킥 수';
COMMENT ON COLUMN teams."own_goals" IS '자책골 수';
COMMENT ON COLUMN teams."cards_yellow_red_against" IS '[상대팀 기준] 경고 누적 퇴장(옐로 2장) 수';
COMMENT ON COLUMN teams."fouls_against" IS '[상대팀 기준] 범한 파울 수';
COMMENT ON COLUMN teams."fouled_against" IS '[상대팀 기준] 당한 파울 수';
COMMENT ON COLUMN teams."offsides_against" IS '[상대팀 기준] 오프사이드 수';
COMMENT ON COLUMN teams."crosses_against" IS '[상대팀 기준] 크로스 시도 수';
COMMENT ON COLUMN teams."interceptions_against" IS '[상대팀 기준] 인터셉트(가로채기) 수';
COMMENT ON COLUMN teams."tackles_won_against" IS '[상대팀 기준] 성공한 태클 수';
COMMENT ON COLUMN teams."pens_won_against" IS '[상대팀 기준] 얻어낸 페널티킥 수';
COMMENT ON COLUMN teams."pens_conceded_against" IS '[상대팀 기준] 내준 페널티킥 수';
COMMENT ON COLUMN teams."own_goals_against" IS '[상대팀 기준] 자책골 수';
COMMENT ON COLUMN teams."gk_games" IS '골키퍼로 출전한 경기 수';
COMMENT ON COLUMN teams."gk_games_starts" IS '골키퍼로 선발 출전한 경기 수';
COMMENT ON COLUMN teams."gk_minutes" IS '골키퍼로 출전한 시간(분)';
COMMENT ON COLUMN teams."gk_goals_against" IS '실점 수(골키퍼 기준)';
COMMENT ON COLUMN teams."gk_goals_against_per90" IS '90분당 실점';
COMMENT ON COLUMN teams."gk_shots_on_target_against" IS '상대의 유효슈팅 수(골키퍼 기준)';
COMMENT ON COLUMN teams."gk_saves" IS '선방 수';
COMMENT ON COLUMN teams."gk_save_pct" IS '선방률(%)';
COMMENT ON COLUMN teams."gk_wins" IS '골키퍼로 출전해 승리한 경기 수';
COMMENT ON COLUMN teams."gk_ties" IS '골키퍼로 출전해 무승부한 경기 수';
COMMENT ON COLUMN teams."gk_losses" IS '골키퍼로 출전해 패배한 경기 수';
COMMENT ON COLUMN teams."gk_clean_sheets" IS '무실점 경기 수(클린시트)';
COMMENT ON COLUMN teams."gk_clean_sheets_pct" IS '무실점 경기 비율(%)';
COMMENT ON COLUMN teams."gk_pens_att" IS '상대의 페널티킥 시도 수(대응)';
COMMENT ON COLUMN teams."gk_pens_allowed" IS '페널티킥 실점 허용 수';
COMMENT ON COLUMN teams."gk_pens_saved" IS '페널티킥 선방 수';
COMMENT ON COLUMN teams."gk_pens_missed" IS '상대가 실축한 페널티킥 수';
COMMENT ON COLUMN teams."gk_pens_save_pct" IS '페널티킥 선방률(%)';
COMMENT ON COLUMN teams."gk_games_against" IS '[상대팀 기준] 골키퍼로 출전한 경기 수';
COMMENT ON COLUMN teams."gk_games_starts_against" IS '[상대팀 기준] 골키퍼로 선발 출전한 경기 수';
COMMENT ON COLUMN teams."gk_minutes_against" IS '[상대팀 기준] 골키퍼로 출전한 시간(분)';
COMMENT ON COLUMN teams."gk_goals_against_against" IS '[상대팀 기준] 실점 수(골키퍼 기준)';
COMMENT ON COLUMN teams."gk_goals_against_per90_against" IS '[상대팀 기준] 90분당 실점';
COMMENT ON COLUMN teams."gk_shots_on_target_against_against" IS '[상대팀 기준] 상대의 유효슈팅 수(골키퍼 기준)';
COMMENT ON COLUMN teams."gk_saves_against" IS '[상대팀 기준] 선방 수';
COMMENT ON COLUMN teams."gk_save_pct_against" IS '[상대팀 기준] 선방률(%)';
COMMENT ON COLUMN teams."gk_wins_against" IS '[상대팀 기준] 골키퍼로 출전해 승리한 경기 수';
COMMENT ON COLUMN teams."gk_ties_against" IS '[상대팀 기준] 골키퍼로 출전해 무승부한 경기 수';
COMMENT ON COLUMN teams."gk_losses_against" IS '[상대팀 기준] 골키퍼로 출전해 패배한 경기 수';
COMMENT ON COLUMN teams."gk_clean_sheets_against" IS '[상대팀 기준] 무실점 경기 수(클린시트)';
COMMENT ON COLUMN teams."gk_clean_sheets_pct_against" IS '[상대팀 기준] 무실점 경기 비율(%)';
COMMENT ON COLUMN teams."gk_pens_att_against" IS '[상대팀 기준] 상대의 페널티킥 시도 수(대응)';
COMMENT ON COLUMN teams."gk_pens_allowed_against" IS '[상대팀 기준] 페널티킥 실점 허용 수';
COMMENT ON COLUMN teams."gk_pens_saved_against" IS '[상대팀 기준] 페널티킥 선방 수';
COMMENT ON COLUMN teams."gk_pens_missed_against" IS '[상대팀 기준] 상대가 실축한 페널티킥 수';
COMMENT ON COLUMN teams."gk_pens_save_pct_against" IS '[상대팀 기준] 페널티킥 선방률(%)';

DROP TABLE IF EXISTS playerse CASCADE;
CREATE TABLE playersE (
    "players_id" SERIAL PRIMARY KEY,
    "player" TEXT,
    "team" TEXT,
    "team_country" TEXT,
    "position" TEXT,
    "age" INTEGER,
    "birth_year" INTEGER,
    "club" TEXT,
    "games" INTEGER,
    "games_starts" INTEGER,
    "minutes" NUMERIC,
    "minutes_90s" NUMERIC,
    "goals" NUMERIC,
    "assists" NUMERIC,
    "goals_assists" NUMERIC,
    "goals_pens" NUMERIC,
    "pens_made" NUMERIC,
    "pens_att" NUMERIC,
    "cards_yellow" NUMERIC,
    "cards_red" NUMERIC,
    "goals_per90" NUMERIC,
    "assists_per90" NUMERIC,
    "goals_assists_per90" NUMERIC,
    "goals_pens_per90" NUMERIC,
    "goals_assists_pens_per90" NUMERIC,
    "shots" NUMERIC,
    "shots_on_target" NUMERIC,
    "shots_on_target_pct" NUMERIC,
    "shots_per90" NUMERIC,
    "shots_on_target_per90" NUMERIC,
    "goals_per_shot" NUMERIC,
    "goals_per_shot_on_target" NUMERIC,
    "minutes_per_game" NUMERIC,
    "minutes_pct" NUMERIC,
    "minutes_per_start" NUMERIC,
    "games_complete" INTEGER,
    "games_subs" INTEGER,
    "minutes_per_sub" NUMERIC,
    "unused_subs" INTEGER,
    "points_per_game" NUMERIC,
    "on_goals_for" NUMERIC,
    "on_goals_against" NUMERIC,
    "plus_minus" NUMERIC,
    "plus_minus_per90" NUMERIC,
    "plus_minus_wowy" NUMERIC,
    "cards_yellow_red" NUMERIC,
    "fouls" NUMERIC,
    "fouled" NUMERIC,
    "offsides" NUMERIC,
    "crosses" NUMERIC,
    "interceptions" NUMERIC,
    "tackles_won" NUMERIC,
    "pens_won" TEXT,
    "pens_conceded" TEXT,
    "own_goals" NUMERIC,
    "gk_games" NUMERIC,
    "gk_games_starts" NUMERIC,
    "gk_minutes" NUMERIC,
    "gk_goals_against" NUMERIC,
    "gk_goals_against_per90" NUMERIC,
    "gk_shots_on_target_against" NUMERIC,
    "gk_saves" NUMERIC,
    "gk_save_pct" NUMERIC,
    "gk_wins" NUMERIC,
    "gk_ties" NUMERIC,
    "gk_losses" NUMERIC,
    "gk_clean_sheets" NUMERIC,
    "gk_clean_sheets_pct" NUMERIC,
    "gk_pens_att" NUMERIC,
    "gk_pens_allowed" NUMERIC,
    "gk_pens_saved" NUMERIC,
    "gk_pens_missed" NUMERIC,
    "gk_pens_save_pct" NUMERIC
);

COMMENT ON COLUMN matches."round" IS '라운드/스테이지 (조별리그, 16강 등)';
COMMENT ON COLUMN matches."gameweek" IS '조별리그 라운드 번호(조별리그 1~3라운드, 토너먼트는 공란)';
COMMENT ON COLUMN matches."dayofweek" IS '요일';
COMMENT ON COLUMN matches."date" IS '경기 날짜';
COMMENT ON COLUMN matches."start_time" IS '경기 시작 시각(현지시각)';
COMMENT ON COLUMN matches."home_team" IS '홈팀(대회 특성상 편의상 지정된 팀, 중립경기 다수)';
COMMENT ON COLUMN matches."away_team" IS '원정팀';
COMMENT ON COLUMN matches."score" IS '최종 스코어 (정규시간+연장 기준, ''홈-원정'' 형식)';
COMMENT ON COLUMN matches."home_score" IS '홈팀 득점 수(정규시간+연장 기준)';
COMMENT ON COLUMN matches."away_score" IS '원정팀 득점 수(정규시간+연장 기준)';
COMMENT ON COLUMN matches."home_pens" IS '승부차기 홈팀 득점 수(승부차기가 없으면 NULL)';
COMMENT ON COLUMN matches."away_pens" IS '승부차기 원정팀 득점 수(승부차기가 없으면 NULL)';
COMMENT ON COLUMN matches."went_to_penalties" IS '승부차기 진행 여부(true/false)';
COMMENT ON COLUMN matches."attendance" IS '관중 수';
COMMENT ON COLUMN matches."venue" IS '경기장';
COMMENT ON COLUMN matches."referee" IS '주심';
COMMENT ON COLUMN matches."home_formation" IS '홈팀 포메이션';
COMMENT ON COLUMN matches."away_formation" IS '원정팀 포메이션';
COMMENT ON COLUMN matches."home_manager" IS '홈팀 감독';
COMMENT ON COLUMN matches."away_manager" IS '원정팀 감독';
COMMENT ON COLUMN matches."home_captain" IS '홈팀 주장';
COMMENT ON COLUMN matches."away_captain" IS '원정팀 주장';
COMMENT ON COLUMN matches."home_possession" IS '홈팀 점유율(%)';
COMMENT ON COLUMN matches."away_possession" IS '원정팀 점유율(%)';
COMMENT ON COLUMN matches."home_sot" IS '홈팀 유효슈팅 수';
COMMENT ON COLUMN matches."away_sot" IS '원정팀 유효슈팅 수';
COMMENT ON COLUMN matches."home_total_shots" IS '홈팀 총 슈팅 수';
COMMENT ON COLUMN matches."away_total_shots" IS '원정팀 총 슈팅 수';
COMMENT ON COLUMN matches."home_saves" IS '홈팀 골키퍼 선방 수';
COMMENT ON COLUMN matches."away_saves" IS '원정팀 골키퍼 선방 수';
COMMENT ON COLUMN matches."home_cards_yellow" IS '홈팀 경고 수';
COMMENT ON COLUMN matches."away_cards_yellow" IS '원정팀 경고 수';
COMMENT ON COLUMN matches."home_cards_red" IS '홈팀 퇴장 수';
COMMENT ON COLUMN matches."away_cards_red" IS '원정팀 퇴장 수';
COMMENT ON COLUMN matches."home_fouls" IS '홈팀 파울 수';
COMMENT ON COLUMN matches."away_fouls" IS '원정팀 파울 수';
COMMENT ON COLUMN matches."home_corners" IS '홈팀 코너킥 수';
COMMENT ON COLUMN matches."away_corners" IS '원정팀 코너킥 수';
COMMENT ON COLUMN matches."home_crosses" IS '홈팀 크로스 수';
COMMENT ON COLUMN matches."away_crosses" IS '원정팀 크로스 수';
COMMENT ON COLUMN matches."home_interceptions" IS '홈팀 인터셉트 수';
COMMENT ON COLUMN matches."away_interceptions" IS '원정팀 인터셉트 수';
COMMENT ON COLUMN matches."home_offsides" IS '홈팀 오프사이드 수';
COMMENT ON COLUMN matches."away_offsides" IS '원정팀 오프사이드 수';
COMMENT ON COLUMN matches."notes" IS '비고(연장전, 승부차기 승리팀 등 특이사항)';
-- ================================
-- 데이터 적재 (psql \copy 사용, 클라이언트 로컬 파일 기준)
-- CSV 헤더 순서 = 테이블 컬럼 순서(SERIAL id 제외)와 동일하므로 컬럼 목록 생략 가능
-- ================================
-- \copy players FROM 'players.csv' WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF8');
-- \copy matches FROM 'matches.csv' WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF8');
-- \copy teams  FROM 'teams.csv'  WITH (FORMAT csv, HEADER true, NULL '', ENCODING 'UTF8');
