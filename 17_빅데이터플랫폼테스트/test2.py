from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()
registered_books = {}

@app.post("/books/register")
def register_book(isbn: str):
    if isbn in registered_books:
        raise Exception("이미 존재하는 값")
    registered_books[isbn] = {"isbn": isbn}
    return {"message": "등록 성공"}

client = TestClient(app, raise_server_exceptions=False)
client.post("/books/register", params={"isbn": "9788937460586"})
response = client.post("/books/register", params={"isbn": "9788937460586"})
print(response.status_code)