# 라이브러리
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier # 의사결정나무 분류
from sklearn.metrics import accuracy_score  # 정확도
import json


def train():
# 펭귄 csv 파일
    df= pd.read_csv('penguins.csv')
    # print(df.head())

    # 결측치 확인 & 제거
    # print(df.isna().sum())
    # df= df.dropna(subset=['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g'])
    # print(df.isna().sum())

    # 모델 학습
    features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g' ]
    X = df[features]
    y = df['species']

    # print(X.shape) # (344, 4)
    # print(y.shape) # (344,)

    X_train, X_valid, y_train, y_valid = train_test_split(
        X, y, test_size=0.25, random_state=42, stratify=y
    )

    # print(X_train.shape)    #(258, 4)
    # print(X_valid.shape)    #(86, 4)
    # print(y_train.shape)    #(258,)
    # print(y_valid.shape)    #(86,)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train) # 학습

    pred = model.predict(X_valid)
    print(accuracy_score(y_valid, pred))    # 0.9883720930232558
    acc = accuracy_score(y_valid, pred)

    # 샘플 확인
    # columns = features로 경고 메세지 삭제
    sample = pd.DataFrame([[41.5,18.5,192,3500]], columns=features)
    prediction = model.predict(sample)
    # 샘플 모델 적합도 코드
    proba = model.predict_proba(sample) 
    confidence = float(proba.max()) 
    print((f'predicted_species: {prediction[0]}, confidence:{confidence}'))   # ['Adelie']
    #모델 저장
    joblib.dump(model, "penguin_model.pkl")

    return{
        "accuracy" : round(acc, 2),
        # 반환 형태에 관한 질문 후 [0] 추가
        "predicted_species" : prediction[0],
        "confidence": round(confidence, 2)
    }

if __name__ == '__main__':
    print(json.dumps(train(), ensure_ascii=False,indent=2))
