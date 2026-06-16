from schema.response import BlogResponse
from schema.request import BlogCreateRequest, BlogUpdateRequest
from fastapi import FastAPI, status, HTTPException
from sqlalchemy import select
from database.db_connection import engine, SessionFactory
from database.orm import Base
from models import Post

Base.metadata.create_all(bind=engine)

app = FastAPI()

posts = []


@app.get(
    '/posts',
    response_model=list[BlogResponse], 
    status_code=status.HTTP_200_OK     
)
def get_posts_handler():
    session = SessionFactory()
    try: # stmt : SQL문을 의미하는 statement의 약자
        stmt = select(Post) # 데이터를 조회하는 쿼리 객체(아직 데이터베이스에는 접근 안했다.)
        # session.execute(stmt) : 쿼리 객체를 실제 데이터베이스에 전달해서 실행
        # .scalars().all() : 실행 결과에서 테이블의 각 행에 대응되는 ORM 객체를 추출해서 리스트로 반환
        posts = session.execute(stmt).scalars().all() # 전체 결과 리스트로 반환
        return posts
    finally: # 예외가 발생하든 안하든 무조건 실행
        session.close()


@app.get(
    '/posts/{post_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def get_post_handler(post_id: int):
    session = SessionFactory()
    try:
        stmt = select(Post).where(Post.id == post_id)
        post = session.execute(stmt).scalars().first() # 첫번째 결과 1개만
        if post:
            return post
        # 없으면 404 에러
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    finally:
        session.close()


@app.post(
    '/posts',
    response_model=BlogCreateRequest,
    status_code=status.HTTP_201_CREATED
)
def create_post_handler(body: BlogCreateRequest): # 요청 body를 자동으로 파싱
    session = SessionFactory()
    try:
        post = Post(
            title = body.title,
            content=body.content,
        )
        session.add(post) # INSERT 준비
        session.commit() # DB에 실제 반영 (commit이 없으면 저장 안됨)
        return post
    finally:
        session.close()


@app.patch(
    '/posts/{post_id}',
    response_model=BlogResponse,
    status_code=status.HTTP_200_OK
)
def update_post_handler(post_id: int, body: BlogUpdateRequest):
    session = SessionFactory()
    try:
        stmt = select(Post).where(Post.id == post_id)
        post = session.execute(stmt).scalars().first()
        if post:
            if body.title is not None:
                post.title = body.title
            if body.content is not None:
                post.content = body.content
            session.commit() # DB에 반영
            return post
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    finally:
        session.close()

@app.delete(
    '/posts/{post_id}',
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_post_handler(post_id: int):
    session = SessionFactory()
    try:
        stmt = select(Post).where(Post.id == post_id)
        post = session.execute(stmt).scalars().first()
        if post:
            session.delete(post) # DELETE 준비
            session.commit() # DB에 실제 반영
            return
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Post not found'
        )
    finally:
        session.close()