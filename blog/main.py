from schema.response import BlogResponse
from schema.request import BlogCreateRequest, BlogUpdateRequest
from fastapi import FastAPI, status, HTTPException

app = FastAPI()

# 임시 데이터
blogs = []

# 전체 게시글 조회
@app.get(
    '/',
    response_model=list[BlogResponse],
    status_code=status.HTTP_200_OK
)
def get_blogs_handler():
    return blogs

# 단일 게시글 조회
@app.get(
    '/{blog_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def get_blog_handler(blog_id: int):
    for blog in blogs:
        if blog['id'] == blog_id:
            return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')

# 게시글 생성
@app.post(
    '/',
    response_model=BlogResponse,
    status_code=status.HTTP_201_CREATED
)
def create_blog_handler(body: BlogCreateRequest):
    new_blog = {
        'id': len(blogs) + 1,
        'title': body.title,
        'content': body.content
    }
    blogs.append(new_blog)
    return new_blog

# 게시글 수정
@app.patch(
    '/{blog_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def update_blog_handler(blog_id: int, body: BlogUpdateRequest):
    for blog in blogs:
        if blog['id'] == blog_id:
            if body.title is not None:
                blog['title'] = body.title
            if body.content is not None:
                blog['content'] = body.content
            return blog
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')

# 게시글 삭제
@app.delete(
    '/{blog_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_blog_handler(blog_id: int):
    for blog in blogs:
        if blog['id'] == blog_id:
            blogs.remove(blog)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Blog not found')