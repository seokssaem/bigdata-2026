import requests


BASE_URL = "http://127.0.0.1:8000"
TIMEOUT = 10


def handle_response(response):

    try:
        data = response.json()

    except ValueError:
        data = response.text

    if response.ok:
        return data

    raise RuntimeError(
        f"API 오류 ({response.status_code})\n{data}"
    )


def health_check():

    response = requests.get(
        f"{BASE_URL}/health",
        timeout=2,
    )

    return response.ok


def get_players(
    team=None,
    position=None,
    search=None,
    sort_by="id",
    sort_order="asc",
    page=1,
    size=20,
):

    params = {
        "sort_by": sort_by,
        "sort_order": sort_order,
        "page": page,
        "size": size,
    }

    if team:
        params["team"] = team

    if position:
        params["position"] = position

    if search:
        params["search"] = search

    response = requests.get(
        f"{BASE_URL}/players",
        params=params,
        timeout=TIMEOUT,
    )

    return handle_response(response)


def get_player(player_id):

    response = requests.get(
        f"{BASE_URL}/players/{player_id}",
        timeout=TIMEOUT,
    )

    return handle_response(response)


def get_matches(
    team=None,
    round_name=None,
):

    params = {}

    if team:
        params["team"] = team

    if round_name:
        params["round"] = round_name

    response = requests.get(
        f"{BASE_URL}/matches",
        params=params,
        timeout=TIMEOUT,
    )

    return handle_response(response)


def get_teams(search=None):

    params = {}

    if search:
        params["search"] = search

    response = requests.get(
        f"{BASE_URL}/teams",
        params=params,
        timeout=TIMEOUT,
    )

    return handle_response(response)


def get_top_scorers(limit=10):

    response = requests.get(
        f"{BASE_URL}/stats/top-scorers",
        params={
            "limit": limit
        },
        timeout=TIMEOUT,
    )

    return handle_response(response)


def get_team_goal_diff():

    response = requests.get(
        f"{BASE_URL}/stats/team-goal-diff",
        timeout=TIMEOUT,
    )

    return handle_response(response)