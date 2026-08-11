import pandas as pd
import numpy as np
import streamlit as st
import statsmodels.api as sm
from data_loader import load_batter

st.title("가설 검증 및 통계 분석")

df = load_batter()

# 독립변수 11개 (OBP, SLG는 데이터 누수 방지를 위해 제외)
FEATURES = ["타석", "타수", "안타", "2루타", "3루타", "홈런", "볼넷", "삼진", "도루", "타점", "득점"]
TARGET = "OPS"

st.subheader("데이터 누수(Data Leakage) 점검")
st.write(
    "OPS(출루율+장타율)를 직접 구성하는 출루율·장타율은 독립변수에서 제외했습니다. "
    "안타, 홈런, 볼넷 등은 OPS 계산의 '원본 재료'이지만 그 자체로는 OPS가 아니므로 독립변수로 사용합니다."
)
st.caption(f"사용 독립변수 ({len(FEATURES)}개): {', '.join(FEATURES)}")

st.divider()

# --- 100타석 이상 필터 ---
min_pa_only = st.checkbox("100타석 이상만 분석에 포함")
analysis_df = df[df["타석"] >= 100] if min_pa_only else df

st.caption(f"분석 대상: {len(analysis_df):,}명 (전체 {len(df):,}명 중)")

X = analysis_df[FEATURES]
y = analysis_df[TARGET]

st.divider()

# --- 상관관계 분석 ---
st.subheader("상관관계 분석")

corr_with_target = X.assign(OPS=y).corr()["OPS"].drop("OPS").sort_values(ascending=False)
st.write("독립변수 - OPS 상관계수")
st.dataframe(corr_with_target.rename("상관계수").to_frame().reset_index(names="변수"), hide_index=True)

st.write("독립변수 간 상관계수 행렬")
corr_matrix = X.corr()
st.dataframe(corr_matrix.style.background_gradient(cmap="RdBu_r", vmin=-1, vmax=1).format("{:.2f}"), hide_index=False)

st.divider()

# --- 가설검정 (F-검정, t-검정) ---
st.subheader("가설검정 결과")
st.write(
    "귀무가설(H0): 타자의 기본 기록은 OPS 예측에 유의한 영향을 미치지 않는다.  \n"
    "대립가설(H1): 타자의 기본 기록은 OPS 예측에 유의한 영향을 미친다."
)

X_c = sm.add_constant(X)
model = sm.OLS(y, X_c).fit()

col1, col2 = st.columns(2)
with col1:
    st.metric("F-통계량", f"{model.fvalue:.2f}")
with col2:
    st.metric("F-검정 p-value", f"{model.f_pvalue:.4g}")

if model.f_pvalue < 0.05:
    st.success("F-검정 p-value < 0.05 → 귀무가설(H0) 기각. 모델 전체가 통계적으로 유의합니다.")
else:
    st.warning("F-검정 p-value ≥ 0.05 → 귀무가설(H0) 기각 실패. 모델 전체 유의성을 확인할 수 없습니다.")

st.write("변수별 t-검정 (개별 유의성)")
t_test_df = pd.DataFrame({
    "계수(coef)": model.params,
    "표준오차(std err)": model.bse,
    "t값": model.tvalues,
    "p-value": model.pvalues,
}).drop("const")
t_test_df["유의(p<0.05)"] = t_test_df["p-value"] < 0.05
t_test_df = t_test_df.reset_index(names="변수")
st.dataframe(t_test_df.style.format({
    "계수(coef)": "{:.4f}",
    "표준오차(std err)": "{:.4f}",
    "t값": "{:.2f}",
    "p-value": "{:.4g}",
}), hide_index=True)

st.caption(f"결정계수 R² = {model.rsquared:.4f}")