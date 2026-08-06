# ====================================================
# 202. 08. 06.  
# 머신러닝실습(회귀_연습문제)
# Page 332.  chapter 08, Section 01,  항공권 가격 예측

# 제출 파일은 다음 1개의 컬럼을 포함해야 한다.
# - pred: 예측값(가격)
# - 제출 파일명: ' result. csv'

# 제출한 모델의 성능은 RMSE 평가지표에 따라 채점한다.
# - 제출 csv 파일명 및 형태: result, csv
# ====================================================

# 1. 라이브러리 불러오기
import pandas as pd

from sklearn.model_selection import train_test_split # 검증 데이터 나누기
from sklearn.ensemble import RandomForestRegressor # 머신러닝 학습 및 평가
from sklearn.metrics import root_mean_squared_error # RMSE(Root Mean Squared Error)


# 2. 파일 불러오기
train = pd.read_csv('p332_flight/flight_train.csv')
test = pd.read_csv('p332_flight/flight_test.csv')


# 3. 탐색적 데이터 분석(EDA)
print('\n === 데이터 크기 확인하기 ===')
print(train.shape)  # (10505, 11)
print(test.shape)   # (4502, 10)


print('\n === 데이터 확인하기(상위 5개) ===')
print(train.head())
print('\n')
print(test.head())
\

print('\n === 데이터 정보(컬럼과 자료형) 확인하기 ===')
print(train.info())
print('\n')
print(test.info())


print('\n === 기초 통계량 확인하기(수치형만) ===') 
print(train.describe())
print('\n')
print(test.describe())


print('\n === 기초 통계량 확인하기(범주형만) ===') 
print(train.describe(include='O'))
print('\n')
print(test.describe(include='O'))


print('\n === 컬럼별 결측치 개수 확인하기 ===')  # 결과 : 결측치 없음
print(train.isnull().sum())
print('\n')
print(test.isnull().sum())
       
print(('\n === target(price)의 기술 통계 ==='))  # 결과 :  평균값이 중앙값(50% )보다 크므로 오른쪽 왜곡이 있다
print(train['price'].describe())

print('\n === 범주형 컬럼만 확인하기 ===')  # 결과 ['airline', 'flight', 'source_city', 'departure_time', 'stops', 'arrival_time', 'destination_city', 'class']
print(train.columns[train.dtypes == object])


# 4. 데이터 전처리
target = train.pop('price')
print('\n === 타켓 데이타 확인 ===' )
print(train.shape)

# 카테고리가 다른 컬럼 찾기 및 삭제하기
cols = train.select_dtypes(include="object").columns
for col in cols:
    set_train = set(train[col])
    set_test = set(test[col])
    same = (set_train == set_test)
    if not same:
        print(f'카테고리가 동일하지 않음 : {col}')

train = train.drop('flight', axis=1)
test = test.drop('flight', axis=1)


# 원-핫 인코딩 :"범주형 변수 → 숫자로 변환"
train = pd.get_dummies(train, dtype=int) # get_dummies() : pandas에서 제공하는 원-핫 인코딩 함수
test = pd.get_dummies(test, dtype=int)   # dtype=int : 결과를 True/False가 아니라 0/1로 보여주기 위해서
print('\n  ===원-핫 인코딩 결과 데이터 확인하기===')
print(train.head())
print(train.head())


# 5. 검증 데이터 나누기
X_tr, X_val, y_tr, y_val = train_test_split(train, target, test_size=0.2, random_state=0)

print('\n === 분할된 데이터 크기 확인 ===')
print(X_tr.shape, X_val.shape, y_tr.shape, y_val.shape) # (8404, 37) (2101, 37) (8404,) (2101,)

# 6. 머신러닝 학습 및 평가
rf = RandomForestRegressor()
rf.fit(X_tr, y_tr) # 학습(훈련)하기
pred=rf.predict(X_val) # 학습이 완료된 랜덤포레스트(Random Forest) 모델을 이용해 검증 데이터(X_val)의 값을 예측
print('\n === 모델이 예측한 항공권 가격 확인하기===')
print(pred) 

# RMSE
result = root_mean_squared_error(y_val, pred) # 실제값(y_val)과 예측값(pred)의 RMSE를 계산
print('\n === RMSE(R^2) 결과 확인하기 ===')
print(result)

# 7. 예측 및 결과 파일 생성
pred = rf.predict(test)
submit = pd.DataFrame({'pred':pred}) # {'pred': pred} --> '컬럼 이름(문자열)' : 데이터
submit.to_csv('p332_flight/result.csv', index=False)

print('\n === 제출파일 확인하기 ====')
print(pd.read_csv('p332_flight/result.csv').head())
