from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient

app = FastAPI()
books = [{"title": "싯다르타"}, {"title": "모순"}]

@app.get("/books/search")
def search_books(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="검색어를 입력하세요")
    results = [b for b in books if keyword in b["title"]]
    return {"count": len(results), "results": results}

client = TestClient(app)

def test_search_books_success():
    response = client.get("/books/search", params={"keyword": "싯다르타"})
    assert response.status_code == 200

def test_search_books_empty_keyword():
    response = client.get("/books/search", params={"keyword": ""})
    assert response.status_code == 400