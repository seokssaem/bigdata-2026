from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_search_books():
    response = client.get(
        "/books/search",
        params={"keyword": "파이썬"}
    )

    assert response.status_code == 200

def test_search_books_empty_keyword():
    response = client.get(
        "/books/search",
        params={"keyword": ""}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "검색어를 입력하세요"
