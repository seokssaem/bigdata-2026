'''
main.py - FastAPI 애플리케이션 진입점
'''
from fastapi import FastAPI
from contextlib import asynccontextmanager
from database.db_connection import engine
from database.orm import Base
from routers.movie import router as movie_router
from routers.favorite import router as favorite_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(movie_router)
app.include_router(favorite_router)
