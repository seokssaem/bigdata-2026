"""
실습 1. 도서 검색 API pytest 테스트 코드

대상 API: GET /books/search?keyword=...
- 검색어가 주어지면 제목에 검색어가 포함된 도서 목록과 개수를 반환 (200)
- 검색어가 비어있으면 400 에러와 안내 메시지를 반환 (400)

FastAPI의 TestClient(starlette 기반)를 사용하여 실제 서버 기동 없이
요청/응답을 검증한다.
"""

from fastapi.testclient import TestClient

from book_api import app

client = TestClient(app)


def test_search_books_success():
    """[정상] 검색어가 주어졌을 때 200 응답과 일치하는 결과를 반환하는지 검증"""
    response = client.get("/books/search", params={"keyword": "파이썬"})

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 2
    assert all("파이썬" in book["title"] for book in data["results"])


def test_search_books_no_match():
    """[정상] 검색 결과가 없어도 200 응답과 count=0, 빈 리스트를 반환하는지 검증"""
    response = client.get("/books/search", params={"keyword": "존재하지않는책"})

    assert response.status_code == 200
    data = response.json()
    assert data["count"] == 0
    assert data["results"] == []


def test_search_books_empty_keyword():
    """[예외] 검색어가 빈 문자열일 때 400 응답과 에러 메시지를 반환하는지 검증"""
    response = client.get("/books/search", params={"keyword": ""})

    assert response.status_code == 400
    assert response.json()["detail"] == "검색어를 입력하세요"


def test_search_books_missing_keyword_param():
    """[예외] keyword 쿼리 파라미터 자체가 누락된 경우 422 응답(FastAPI 자동 검증)을 반환하는지 검증"""
    response = client.get("/books/search")

    assert response.status_code == 422
