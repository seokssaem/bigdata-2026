from fastapi import FastAPI, status, HTTPException
from schema.response import BlogResponse
from schema.request import BlogCreateRequest, BlogUpdateRequest

app = FastAPI()

posts = [
    {'id':1, 'title':'첫번째 제목', 'content':'aaa'},
    {'id':2, 'title':'두번째 제목', 'content':'bbb'},
    {'id':3, 'title':'세번째 제목', 'content':'ccc'},
]

@app.get(
    '/',
    response_model=list[BlogResponse],
    status_code=status.HTTP_200_OK
)
def get_post_handler():
    return posts

@app.get(
    '/{post_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def get_post_handler(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Todo not found')

@app.post(
    '/',
    response_model=BlogCreateRequest,
    status_code=status.HTTP_201_CREATED
)
def create_post_handler(body: BlogCreateRequest):
    new_post = {
        'id': len(posts) + 1,
        'title': body.title,
        'content': body.content,
    }
    posts.append(new_post)
    return new_post

@app.patch(
    '/{post_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def update_post_handler(post_id: int, body: BlogUpdateRequest):
    for post in posts:
        if post['id'] == post_id:
            if body.title is not None:
                post['title'] = body.title
            if body.content is not None:
                post['content'] = body.content
            return post
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Post not found')

@app.delete(
    '/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post_handler(post_id: int):
    for post in posts:
        if post['id'] == post_id:
            posts.remove(post)
            return
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)