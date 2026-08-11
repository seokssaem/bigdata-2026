"""
make_model.py

작업일자: 2026-08-11
작업자: 김나현
목적 : '홈페이지주소','행사기간','버스정류장수','지하철유무'를 입력하여 '방문객수'를 예측하는 선형회귀 모델을 학습 및 평가, 저장한다.
"""
# 라이브러리 불러오기
from pathlib import Path # 경로 설정
import json 
import joblib # 학습이 끝난 파이프라인(전처리+모델)을 파일로 저장하고 나중에 다시 불러오기 위해 사용

import pandas as pd
from sklearn.compose import ColumnTransformer # 열마다 다른 전처리를 동시에 적용
from sklearn.linear_model import LinearRegression
from sklearn.impute import SimpleImputer # 결측치를 대표값으로 채운다.
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score # 평가지표들(분류)
from sklearn.model_selection import train_test_split # 데이터 분할
from sklearn.pipeline import make_pipeline, Pipeline # 전처리+모델학습을 하나로 묶어서 학습/예측
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import mean_absolute_error, mean_squared_error, root_mean_squared_error, r2_score

# 데이터 경로 설정
# __file__ : 현재 이 .py의 파일 자신의 경로
# .resolve() : 상대경로를 절대경로로 바꿔준다. (어디서 실행하든 안전)
# .parent : 파일이 들어있는 폴더
HERE = Path(__file__).resolve().parent
DATA_PATH = HERE/'data'/'전국문화축제정보정리_raw.csv'

# 학습된 모델과 평가지표를 이 파일에 있는 폴더(HERE) 바로 아래에 저장
MODEL_PATH = HERE / 'festival_model.joblib'
METRICS_PATH = HERE / 'metrics.json'

# 모델 입력으로 사용할 열(feature) 목록을 명시적으로 나열
FEATURE = ['홈페이지주소','행사기간','버스정류장수','지하철유무']

# 예측하려고 하는 정답(target) 열
TARGET = '방문객수'


# 파이프라인 구성
NUMERIC = [
    '행사기간',
    '버스정류장수',
    '홈페이지주소',
    '지하철유무'
]

def build_pipeline() -> Pipeline:

    # --- 숫자형 ---
    numeric_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    # --- 컬럼별 전처리 ---
    preprocessor = ColumnTransformer([
        ('numeric', numeric_pipe, NUMERIC),
    ])

    # --- 모델 ---
    model = LinearRegression()

    return Pipeline([
        ('preprocess', preprocessor),
        ('model', model)
    ])

def train() -> dict:
    """재현 가능한 분할로 모델을 학습하고, 실무 설명용 지표를 반환한다."""

    # CSV 파일을 읽어 데이터프레임으로 저장
    data = pd.read_csv(DATA_PATH)
    data = data.dropna(subset=['방문객수', '광역시도', '버스정류장수'])

    data['홈페이지주소'] = data['홈페이지주소'].notnull().astype(int)
    data['지하철유무'] = data['지하철유무'].replace({'Y': 1, 'N': 0}).astype(int)

    # 입력(X), 정답(y) 분리
    X = data[FEATURE]
    y = data[TARGET]

    # 학습용 / 평가용 데이터 분할 --> 전체의 25%를 평가용
    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y,test_size=0.2
    )

    # 파이프라인 생성 후 학습 데이터로 학습

    pipeline = build_pipeline() # 함수 호출
    pipeline.fit(X_train, y_train) # 학습

    pred = pipeline.predict(X_valid)

    # 보고용으로 핵심 자료만 정리
    metrics = {
        'test_rows': len(X_valid),
        'MAE' : mean_absolute_error(y_valid, pred),
        'MSE' : mean_squared_error(y_valid, pred),
        'RMSE' : root_mean_squared_error(y_valid, pred),
        'r2_score' : r2_score(y_valid, pred)
    }

    # 학습된 파이프라인(전처리+모델) 파일로 저장
    joblib.dump(pipeline, MODEL_PATH)

    return metrics

if __name__ == '__main__':
    # 이 파일을 직접 python train.py 로 실행했을 때만 동작
    print(train())
