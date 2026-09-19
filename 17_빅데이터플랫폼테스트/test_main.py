from fastapi.testclient import TestClient
from main import app  # FastAPI app 인스턴스가 정의된 모듈 경로에 맞게 수정

client = TestClient(app)


def test_search_book_success():
    response = client.get("/books/search", params={"keyword": "오디세이"})
    assert response.status_code == 200

    data = response.json()

    assert "count" in data
    assert "results" in data
    assert data["count"] == len(data["results"])

def test_search_book_noname():
    response = client.get("/books/search", params={"keyword": ""})
    assert response.status_code == 400

    assert "검색어를 입력하세요" in response.json()["detail"]