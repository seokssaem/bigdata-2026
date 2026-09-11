from fastapi import FastAPI, HTTPException

app = FastAPI()

# 테스트용 도서 데이터
books = [
    {"id": 1, "title": "파이썬 프로그래밍", "author": "홍길동"},
    {"id": 2, "title": "파이썬으로 배우는 자료구조", "author": "이순신"},
    {"id": 3, "title": "자바의 정석", "author": "김영한"},
]


@app.get("/books/search")
def search_books(keyword: str):
    if not keyword:
        raise HTTPException(status_code=400, detail="검색어를 입력하세요")
    results = [b for b in books if keyword in b["title"]]
    return {"count": len(results), "results": results}
