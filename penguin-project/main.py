from fastapi import FastAPI, HTTPException, status
import joblib
from pydantic import BaseModel
import numpy as np
import os

class Featureinput(BaseModel):
    bill_length_mm:float
    bill_depth_mm:float
    flipper_length_mm:float
    body_mass_g:float


app = FastAPI(
    title='펭귄 예측'
)


# 모델링으로 만든 pkl파일 불러오기
# pkl를 어떻게 적용하는지 질문
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(BASE_DIR, "penguin_model.pkl")
try:
    model = joblib.load(PATH)
    print('로드 성공')
except Exception as e:
    print('로드 실패 ')
    model = None

@app.get("/")
def root():
    return{'message': '서버 실행'}   


@app.get('/model-info/')
def input_model_size(bill_length_mm, bill_depth_mm, flipper_length_mm, body_mass_g):
    return {"부리 길이": bill_length_mm,
            "부리 깊이": bill_depth_mm,
            "날개 길이": flipper_length_mm,
            "몸무게" : body_mass_g
            }


# 이 부분은 거의 다 물어보고 했어요
# features에 input_model_size -> Featureinput으로 변경
@app.post('/predict/')
def predict(features: Featureinput):
    if model is None:
        # 모델 로드 안 되었을 때 HTTP오류 코드 몇 번인지 질문 -> 500 작성
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail='모델이 로드되지 않았습니다.'
        )

    # np.array() -> numpy 배열로 바꿔줌
    X = np.array([[
        features.bill_length_mm,
        features.bill_depth_mm,
        features.flipper_length_mm,
        features.body_mass_g
    ]])

    prediction = model.predict(X)

    return{
        "입력": features,
        # model.predict(X)가 numpy 배열을 반환 -> prediction[0]도 numpy형태로 반환 가능성 높음 ->
        # FastAPI가 Json을 직렬화 하다 에러 나는 경우 발생 -> str로 형변환
        "예측": str(prediction[0])
    }