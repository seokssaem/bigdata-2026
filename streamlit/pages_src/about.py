import streamlit as st
import pandas as pd

st.title("소개")

st.write("KBO 타자의 기본 경기 기록을 이용해 공격력 종합 지표인 OPS를 예측하는 머신러닝 회귀 모델 개발 프로젝트입니다.")

st.divider()

st.subheader("프로젝트 목적")
st.write(
    "OPS(On-base Plus Slugging)는 타자의 공격력을 종합적으로 평가하는 대표적인 지표이지만, "
    "경기 전에는 알 수 없습니다.  \n선수의 기본 타격 기록을 이용해 OPS를 예측하는 모델을 개발하고, "
    "어떤 기록이 OPS에 가장 큰 영향을 미치는지 분석합니다."
)

st.subheader("분석 가설")
st.write(
    "**H0(귀무가설)**: 타자의 기본 기록은 OPS 예측에 유의한 영향을 미치지 않는다.  \n"
    "**H1(대립가설)**: 타자의 기본 기록은 OPS 예측에 유의한 영향을 미친다."
)

st.divider()

st.subheader("데이터 및 변수")
col1, col2 = st.columns(2)
with col1:
    st.write("**데이터**")
    st.write("- 2025년도 KBO 타자 정규시즌 기록")
    st.write("- 표본 신뢰도 확보를 위해 100타석 이상 선수만 분석 대상으로 선정 가능")
with col2:
    st.write("**변수**")
    st.write("- 독립변수(11개): 타석, 타수, 안타, 2루타, 3루타, 홈런, 볼넷, 삼진, 도루, 타점, 득점")
    st.write("- 종속변수: OPS")

st.caption(
    "출루율(OBP)·장타율(SLG)은 OPS 계산에 직접 쓰이는 값이라 독립변수에 포함하면 "
    "종속변수를 그대로 재구성하는 데이터 누수(Data Leakage) 문제가 생길 수 있어 제외했습니다."
)

st.divider()

st.subheader("모델 개발")
model_col1, model_col2 = st.columns(2)
with model_col1:
    st.write("**Linear Regression**")
    st.write("변수 간 선형 관계를 확인할 수 있고 결과 해석이 쉬운 Baseline 모델")
with model_col2:
    st.write("**Random Forest Regressor**")
    st.write("비선형 관계와 변수 간 복잡한 상호작용을 반영할 수 있는 앙상블 모델")

st.write("Train : Test = 80% : 20%로 분할하고, 5-Fold 교차검증으로 일반화 성능을 함께 확인했습니다.")

st.divider()

st.subheader("성능 평가 결과 (100타석 이상, 5-Fold CV 기준)")
perf_df = pd.DataFrame({
    "모델": ["Linear Regression", "Random Forest Regressor"],
    "Test MAE": [0.0375, 0.0528],
    "Test RMSE": [0.0541, 0.0628],
    "Test R²": [0.7425, 0.6533],
    "CV R² 평균": [0.7789, 0.6451],
    "CV R² 표준편차": [0.0357, 0.0641],
    "CV MAE 평균": [0.0352, 0.0496],
})
st.dataframe(perf_df, hide_index=True)

st.subheader("변수 영향력")
imp_col1, imp_col2 = st.columns(2)
with imp_col1:
    st.write("**Linear Regression 주요 변수**")
    st.write("1. 홈런\n2. 3루타\n3. 안타")
with imp_col2:
    st.write("**Random Forest 주요 변수**")
    st.write("1. 타점\n2. 홈런\n3. 2루타")

st.write("두 모델 모두 홈런, 2루타, 3루타 등 장타력과 관련된 기록이 OPS 예측에 중요한 역할을 하는 것으로 나타났습니다.")

st.divider()

st.subheader("결론")
st.write(
    "타자의 기본 경기 기록만으로도 OPS를 상당 수준 설명할 수 있었으며, 특히 장타 관련 지표의 영향력이 두드러졌습니다. "
    "이번 데이터에서는 OPS와 기본 기록 사이의 관계가 비교적 선형적이어서, Linear Regression이 Random Forest보다 "
    "높은 R²를 기록했습니다."
)
st.success("가설 검정 결과: 귀무가설(H0) 기각, 대립가설(H1) 채택")