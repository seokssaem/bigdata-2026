import uuid

import pytest
from fastapi.testclient import TestClient

import models
from database import SessionLocal
from main import app

# NOTE: 이 테스트는 .env 의 DATABASE_URL 이 가리키는 실제 PostgreSQL 이 필요합니다.
# 테스트가 만든 사용자/프로젝트/회의/업무는 fixture 종료 시 삭제합니다.


# ------------------------------------------------------------
# 로그인 없이 접근하면 막혀야 하는 엔드포인트
# ------------------------------------------------------------
PROTECTED_API = [
    ("GET", "/meetings"),
    ("POST", "/meetings"),
    ("GET", "/meetings/1"),
    ("PUT", "/meetings/1"),
    ("DELETE", "/meetings/1"),
    ("GET", "/meetings/1/audio"),
    ("GET", "/meetings/1/calendar.ics"),
    ("GET", "/tasks"),
    ("POST", "/tasks"),
    ("GET", "/tasks/dashboard"),
    ("GET", "/tasks/calendar"),
    ("GET", "/tasks/calendar.ics"),
    ("GET", "/tasks/latest-meeting-info"),
    ("GET", "/tasks/1"),
    ("PUT", "/tasks/1"),
    ("POST", "/tasks/1/toggle"),
    ("DELETE", "/tasks/1"),
    ("POST", "/api/user/profile-image"),
]


@pytest.mark.parametrize("method,path", PROTECTED_API)
def test_api_requires_login(method, path):
    # 쿠키가 공유되지 않도록 요청마다 새 클라이언트 사용
    response = TestClient(app).request(method, path)
    # 인증 의존성은 본문 검증보다 먼저 실행되므로 항상 401 이어야 함
    assert response.status_code == 401


@pytest.mark.parametrize("path", [
    "/views/dashboard",
    "/views/meetings",
    "/views/meetings/new",
    "/views/calendar",
    "/views/tasks/new",
    "/tasks/calendar-view",
])
def test_pages_redirect_to_login(path):
    response = TestClient(app).get(path, follow_redirects=False)
    assert response.status_code == 303
    assert response.headers["location"] == "/views/login"


def test_login_page_is_public():
    assert TestClient(app).get("/views/login").status_code == 200


# ------------------------------------------------------------
# 실제 사용자 2명으로 소유자 격리 검증
# ------------------------------------------------------------
def _register_and_login(email: str):
    client = TestClient(app)
    password = "pw-12345-test"

    r = client.post("/users/", json={"name": "tester", "email": email, "password": password})
    assert r.status_code == 201, r.text

    r = client.post("/auth/login", json={"email": email, "password": password})
    assert r.status_code == 200, r.text
    body = r.json()

    # 쿠키(Secure 설정 여부와 무관하게) 대신 Bearer 헤더로 인증
    client.headers["Authorization"] = f"Bearer {body['access_token']}"
    return client, body["user"]["id"]


@pytest.fixture
def two_users():
    suffix = uuid.uuid4().hex[:8]
    a, a_id = _register_and_login(f"a_{suffix}@test.example")
    b, b_id = _register_and_login(f"b_{suffix}@test.example")

    yield a, b

    # 정리: 테스트가 만든 데이터 삭제 (FK 순서: 업무/결정 → 회의 → 프로젝트 → 사용자)
    db = SessionLocal()
    try:
        user_ids = [a_id, b_id]
        project_ids = [
            p.id for p in db.query(models.Project).filter(models.Project.owner_id.in_(user_ids))
        ]
        meeting_ids = []
        if project_ids:
            meeting_ids = [
                m.id for m in db.query(models.Meeting).filter(models.Meeting.project_id.in_(project_ids))
            ]
        if meeting_ids:
            db.query(models.ActionItem).filter(
                models.ActionItem.meeting_id.in_(meeting_ids)
            ).delete(synchronize_session=False)
            db.query(models.Decision).filter(
                models.Decision.meeting_id.in_(meeting_ids)
            ).delete(synchronize_session=False)
            db.query(models.Meeting).filter(
                models.Meeting.id.in_(meeting_ids)
            ).delete(synchronize_session=False)
        if project_ids:
            db.query(models.Project).filter(
                models.Project.id.in_(project_ids)
            ).delete(synchronize_session=False)
        db.query(models.User).filter(models.User.id.in_(user_ids)).delete(synchronize_session=False)
        db.commit()
    finally:
        db.close()


def test_dashboard_for_logged_in_user(two_users):
    a, _ = two_users
    response = a.get("/tasks/dashboard")
    assert response.status_code == 200
    data = response.json()
    assert data["total_meetings"] == 0
    assert "tasks" in data


def test_other_users_data_is_invisible(two_users):
    a, b = two_users

    project_id = a.post("/projects/", json={"name": "A project"}).json()["id"]

    r = a.post("/meetings", json={
        "project_id": project_id, "title": "A meeting", "meeting_date": "2026-10-08",
    })
    assert r.status_code == 201, r.text
    meeting_id = r.json()["id"]

    r = a.post("/tasks", json={"meeting_id": meeting_id, "task": "A task"})
    assert r.status_code == 201, r.text
    task_id = r.json()["id"]

    # 소유자는 접근 가능
    assert a.get(f"/meetings/{meeting_id}").status_code == 200
    assert a.get(f"/tasks/{task_id}").status_code == 200
    toggled = a.post(f"/tasks/{task_id}/toggle")
    assert toggled.status_code == 200
    assert toggled.json()["status"] == "completed"

    # 다른 사용자는 존재 자체를 알 수 없어야 함 (404)
    for method, path in [
        ("GET", f"/meetings/{meeting_id}"),
        ("PUT", f"/meetings/{meeting_id}"),
        ("DELETE", f"/meetings/{meeting_id}"),
        ("GET", f"/meetings/{meeting_id}/audio"),
        ("GET", f"/meetings/{meeting_id}/calendar.ics"),
        ("POST", f"/meetings/{meeting_id}/analyze"),
        ("GET", f"/tasks/{task_id}"),
        ("POST", f"/tasks/{task_id}/toggle"),
        ("DELETE", f"/tasks/{task_id}"),
    ]:
        kwargs = {"json": {"title": "hacked"}} if method == "PUT" else {}
        response = b.request(method, path, **kwargs)
        assert response.status_code == 404, f"{method} {path} -> {response.status_code}"

    # 목록/집계에도 섞여 나오지 않음
    assert b.get("/meetings").json() == []
    assert b.get("/tasks").json() == []
    assert b.get("/tasks/calendar").json() == []
    assert b.get("/tasks/dashboard").json()["total_meetings"] == 0

    # 남의 프로젝트에 회의 만들기 불가
    r = b.post("/meetings", json={
        "project_id": project_id, "title": "intrusion", "meeting_date": "2026-10-08",
    })
    assert r.status_code == 404

    # 남의 회의에 업무 붙이기 불가 (본인 회의가 없으므로 400)
    r = b.post("/tasks", json={"meeting_id": meeting_id, "task": "intrusion"})
    assert r.status_code == 400

    # 원본은 그대로
    assert a.get(f"/tasks/{task_id}").json()["task"] == "A task"
