'''
main.py

main 파일 실행 → `uvicorn main:app --reload`
'''
from fastapi import FastAPI
from database import Base, engine
from routers.ingredient import router as ingredient_router

Base.metadata.create_all(engine)

app = FastAPI(title='냉장고 관리 API')

app.include_router(ingredient_router)

@app.get('/', summary='냉장고 관리 API가 실행 중인지 확인합니다.')
async def root():
    return {"message": '냉장고 관리 API 서버가 정상 작동 중입니다.'}