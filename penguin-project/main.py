from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import pandas as pd

# 1. FastAPI 앱 객체 생성
app = FastAPI(
    title='penguin Species predictor API',
    description='펭귄의 신체 데이터를 기반으로 종을 예측하고 모델 정보를 제공하는 API입니다.',
    version='1.0.0'
)

# 2. 머신러닝 모델 로드
MODEL_PATH = 'penguin_model.pkl'
FEATURES = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']

try:
    model = joblib.load(MODEL_PATH)
except FileNotFoundError:
    print(f"⚠️ 경고: '{MODEL_PATH}'파일이 없습니다. train.py를 실행하여 모델을 먼저 생성하세요.")
    model = None

# 3. 데이터 입력을 위한 pydantic 스키마 정의
class Penguininput(BaseModel):
    bill_length_mm: float = Field(..., description='부리 길이(mm)', examples=[40.0])
    bill_depth_mm: float = Field(..., description='부리 깊이(mm)', examples=[18.0])
    flipper_length_mm:int = Field(..., description='날개 길이(mm)', examples=[190])
    body_mass_g: int= Field(..., description='몸무게(g)', examples=[3500])

# 4. [GET] / 엔드포인트
@app.get('/')
def read_root():
    return {
        'status':'active',
        'message':'펭귄 예측 FastAPI 서버가 정상 작동 중입니다.',
        'docs_url': 'http://127.0.0'
    }

# 5. [GET] / model-info 엔드포인트
@app.get('/model-info')
def get_model_info():
    if model is None:
        raise HTTPException(status_code=500, detail='서버에 로드된 모델이 없습니다.')

    model_name = model.__class__.__name__

    return {
        'model_type': model_name,
        'input_features': FEATURES,
        'target_variable': 'species',
        'status': 'ready'
    }

# 6. [Post] / predict 엔드포인트
@app.post('/predict')
def predict_penguin(data: Penguininput):
    if model is None:
        raise HTTPException(status_code=500, detail='서버에 학습된 모델 파일이 존재하지 않습니다.')

    try:
        new_data = pd.DataFrame([{
            'bill_length_mm': data.bill_length_mm,
            'bill_depth_mm': data.bill_depth_mm,
            'flipper_length_mm': data.flipper_length_mm,
            'body_mass_g': data.body_mass_g
        }])

        prediction = model.predict(new_data)

        return {
            'status': 'success',
            'prediction': prediction[0]
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=f'예측 수행 중 오류 발생: {str(e)}')

if __name__ == '__main__':
    import uvicorn
    # 🎯 'main.py:app'에서 '.py'를 제거하고 'main:app'으로 수정합니다.
    uvicorn.run('main:app', host='127.0.0.1', port=8000, reload=True)