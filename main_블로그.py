from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CreatePostRequest(BaseModel):
    title: str
    content: str


class UpdatePostRequest(BaseModel):
    title: str
    content: str

class PostResponse(BaseModel):
    id: int
    title: str
    content: str


class MessageResponse(BaseModel):
    message: str

posts = [
    {
        "id": 1,
        "title": "첫 번째 게시글",
        "content": "안녕하세요."
    }
]

@app.get("/posts", response_model=list[PostResponse])
def get_posts():
    return posts

@app.get("/posts/{post_id}", response_model=PostResponse)
def get_post(post_id: int):

    for post in posts:
        if post["id"] == post_id:
            return post

    raise HTTPException(
        status_code=404,
        detail="게시글을 찾을 수 없습니다."
    )

@app.post("/posts", response_model=PostResponse)
def create_post(request: CreatePostRequest):

    new_id = max([post["id"] for post in posts], default=0) + 1

    new_post = {
        "id": new_id,
        "title": request.title,
        "content": request.content
    }

    posts.append(new_post)

    return new_post

@app.put("/posts/{post_id}", response_model=PostResponse)
def update_post(post_id: int, request: UpdatePostRequest):

    for post in posts:
        if post["id"] == post_id:

            post["title"] = request.title
            post["content"] = request.content

            return post

    raise HTTPException(
        status_code=404,
        detail="게시글을 찾을 수 없습니다."
    )

@app.delete("/posts/{post_id}", response_model=MessageResponse)
def delete_post(post_id: int):

    for post in posts:
        if post["id"] == post_id:

            posts.remove(post)

            return {
                "message": "게시글이 삭제되었습니다."
            }

    raise HTTPException(
        status_code=404,
        detail="게시글을 찾을 수 없습니다."
    )