from fastapi import FastAPI, HTTPException


app = FastAPI()

books = [{"id": 1, "title": "오디세이"}]

@app.get("/books/search")
def search_books(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="검색어를 입력하세요")
    results = [b for b in books if keyword in b["title"]]
    return {"count": len(results), "results": results}