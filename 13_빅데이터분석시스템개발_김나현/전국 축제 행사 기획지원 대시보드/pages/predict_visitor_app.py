"""
predict_visitor_app.py

작업일자: 2026-08-11
작업자: 김나현
목적: train.py로 만든 festival_model.joblib를 실제로 사용하는 사용자 화면 코드 (웹페이지 화면), 시각적
        조건에 따른 축제 방문자수를 예측한다.
"""
# 라이브러리 불러오기
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# 경로 설정
MODEL_PATH = Path(__file__).resolve().parent.parent /'input'/'festival_model.joblib'

st.title('🎡 지역축제 방문객 수 예측 시스템')
st.caption('지역축제의 방문객 규모를 예측하여 지자체의 축제 운영 및 계획 수립을 지원합니다.')

# 모델파일이 존재하는지 확인
if not MODEL_PATH.exists():
    st.error('모델 파일이 없습니다. 터미널에서 `python make_model.py`를 먼저 실행하세요.')
    st.stop() # 이 지점에서 스크립트 실행을 멈춘다. 추가 에러 방지

# 저장했던 전처리 + 모델 그대로 복원
model = joblib.load(MODEL_PATH)

with st.form('customer'):
    duration = st.number_input('행사기간',0,100,3)
    bus = st.number_input('버스정류장수',0,100000, 10000)
    subway = st.checkbox('지하철유무')
    site = st.checkbox('SNS 및 홈페이지 유무')
    
    # 폼 안에서 유일하게 실행을 시작하게 하는 버튼
    submitted = st.form_submit_button('방문객수 예측')

# 버튼을 클릭 했다면
if submitted:
    # 사용자가 입력한 값들로 1행짜리 데이터 프레임 생성
    row = pd.DataFrame([{
        '행사기간': duration,
        '버스정류장수' : bus,
        '홈페이지주소' : int(site),
        '지하철유무' : int(subway),
    }])

    # predict_proba(row): [[비이탈 확률, 이탈 확률]] 형태의 2차원 배열 반환
    # [0,1] 0번째 행(유일한 입력 고객), 1번째 열 (이탈=1일 확률)
    pred = model.predict(row)[0]

    # st.metric 위젯 : 큰 숫자 형태로 강조 표시
    st.metric(
    label="예상 방문객 수",
    value=f"{pred:,.0f}명")

    if pred < 633445:
        level = "상대적으로 적은 규모"
    elif pred < 867112:
        level = "평균적인 규모"
    elif pred < 1355700:
        level = "큰 규모"
    else:
        level = "매우 큰 규모"

    st.info(f"현재 데이터 기준 **{level}**의 방문객 규모입니다.")



    