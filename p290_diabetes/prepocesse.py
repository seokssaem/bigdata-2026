# ===============================================
# 202. 08. 05.  이진분류 연습문제 - 성능개선(심화)
# ===============================================

# 라이브러리 불러오기
import pandas as pd

# 파일 불러오기
train =pd.read_csv('diabetes\diabetes_train.csv')
test = pd.read_csv('diabetes\diabetes_test.csv')

# 데이터 전처리
target =train.pop('Outcome')

from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()
train = scaler.fit_transform(train)
test = scaler.transform(test)

# 검증데이터 나누기
from sklearn.model_selection import train_test_split
X_tr, X_val, y_tr, y_val = train_test_split(train, target, test_size=0.2, random_state=0)

# 머신러닝 학습
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(max_depth=5, n_estimators=500, random_state=0)
rf.fit(X_tr, y_tr)
pred = rf.predict_proba(X_val)
print("=== 랜덤포레스트 결과보기 ===")
print(pred[:5])

# 머신러닝 평가
from sklearn.metrics import roc_auc_score
roc_auc = roc_auc_score(y_val, pred[:,1])
print("=== roc_auc 결과보기 ===")
print( roc_auc)

# 예측 및 결과 파일 생성
pred = rf.predict_proba(test)
submit = pd.DataFrame({'pred':pred[:,1]})
submit.to_csv("diabetes/result1.csv", index=False)
