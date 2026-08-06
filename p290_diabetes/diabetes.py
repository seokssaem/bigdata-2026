# ==============================================================================================================================================================
# 202. 08. 05.  이진분류 연습문제 - 베이스라인(기초)
# ==============================================================================================================================================================
"""
환자의 당뇨병 여부를 예측하시오.
  · 제공된 데이터 목록: diabetes train. csv, diabetes test. csv
  · 예측할 컬럼: Outcome (0: 정상 , 1: 당뇨병)

학습용 데이터(train)를 이용해 환자의 당뇨병을 예측하는 모델을 만든 후 이를 평가용 데이터(test)에 적용해 얻은 예측값을 다음과 같은 형식의 csv 파일로 생성하시오.

제출 파일은 다음 1개의 컬럼을 포함해야 한다.
  ·pred: 예측값(당뇨병일 확률)
  · 제출파일명: ' result. csv'

제출한 모델의 성능은 ROC-AUC 평가지표에 따라 채점한다.
"""

# ===================
# 라이브러리 불러오기
# ===================
import pandas as pd

# ===================
# 데이터 불러오기
# ===================

train = pd.read_csv('diabetes/diabetes_train.csv')
test = pd.read_csv('diabetes/diabetes_test.csv')

# ======================
# 탐색적 데이터 분석하기
# ======================

# print('=== 데이터 크기 ===')
# print(train.shape, test.shape)  # 결과 : (614, 9) (154, 8)

# print('=== 데이터 샘플 ===')
# print(train.head())
# print("\n")
# print(test.head())

# print('=== 데이터 정보(자료형) ===')
# print(train.info())   # 결과 : 모두 수치형
# print("\n")
# print(test.info())    # 결과 : 모두 수치형

# print('=== 결측치 수 ===')
# print(train.isnull().sum())  # 결과 : 0
# print("\n")
# print(test.isnull().sum())  # 결과 : 0

# print('=== target 빈도 ===')
# print(train['Outcome'].value_counts())  # 결과: 0 --> 403, 1 --> 211

# ======================
# 데이터 전처리
# ======================
target = train.pop('Outcome')
# print(target)

# ======================
# 검증 데이터 나누기
# ======================
from sklearn.model_selection import train_test_split
X_tr, X_val, y_tr, y_val = train_test_split(train, target, test_size=0.2, random_state=0)

# print('=== 분할된 데이터 크기 확인하기 ===')
# print(X_tr.shape, X_val.shape, y_tr.shape, y_val.shape)  # 결과 : (491, 8) (123, 8) (491,) (123,)

# ======================
# 머신러닝 학습 및 평가
# ======================
from sklearn.ensemble import RandomForestClassifier
rf = RandomForestClassifier(random_state=0)
rf.fit(X_tr, y_tr)
pred = rf.predict_proba(X_val)

print('=== 예측 결과 확인(처음부터 5개만 확인) ===')
print(pred[:5])

from sklearn.metrics import roc_auc_score
roc_auc = roc_auc_score(y_val, pred[:, 1])

print('=== roc_auc 결과 확인 ===')
print(roc_auc)  # 결과 : 0.8002739726027398

# ======================
# 예측 및 결과 파일 생성
# ======================
pred = rf.predict_proba(test)
submit = pd.DataFrame({'pred':pred[:,1]})
submit.to_csv("diabetes/result.csv", index=False)

# ======================
# 생성 파일 확인하기
# ======================
print('=== result.csv  확인하기 ===')
print(pd.read_csv("diabetes/result.csv").head()) 
