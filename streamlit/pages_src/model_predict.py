import pandas as pd
import numpy as np
import streamlit as st
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from data_loader import load_batter

st.title("OPS 예측 모델")

df = load_batter()

FEATURES = ["타석", "타수", "안타", "2루타", "3루타", "홈런", "볼넷", "삼진", "도루", "타점", "득점"]
TARGET = "OPS"

# --- 100타석 이상 필터 ---
min_pa_only = st.checkbox("100타석 이상만 학습에 포함")
model_df = df[df["타석"] >= 100] if min_pa_only else df

st.caption(f"학습 대상: {len(model_df):,}명 (전체 {len(df):,}명 중)")

X = model_df[FEATURES]
y = model_df[TARGET]

st.divider()

# --- Train/Test 분할 설정 ---
st.subheader("Train/Test 분할 및 교차검증 설정")

col1, col2 = st.columns(2)
with col1:
    test_size = st.slider("Test 비율", min_value=0.1, max_value=0.5, value=0.2, step=0.05)
with col2:
    cv_folds = st.slider("교차검증 Fold 수", min_value=3, max_value=10, value=5, step=1)

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=42)

st.caption(f"Train {len(X_train):,}명 / Test {len(X_test):,}명")

st.divider()

# --- 모델 학습 ---
st.subheader("모델 학습 및 성능 비교")

lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_pred = lr_model.predict(X_test)

rf_model = RandomForestRegressor(n_estimators=200, random_state=42)
rf_model.fit(X_train, y_train)
rf_pred = rf_model.predict(X_test)

def get_metrics(y_true, y_pred):
    mae = mean_absolute_error(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2

lr_mae, lr_rmse, lr_r2 = get_metrics(y_test, lr_pred)
rf_mae, rf_rmse, rf_r2 = get_metrics(y_test, rf_pred)

# 교차검증 (R² 기준) - shuffle=True로 데이터를 섞어서 fold를 나눔 (팀원 코드와 동일 조건)
cv_splitter = KFold(n_splits=cv_folds, shuffle=True, random_state=42)
lr_cv_r2 = cross_val_score(LinearRegression(), X, y, cv=cv_splitter, scoring="r2")
rf_cv_r2 = cross_val_score(RandomForestRegressor(n_estimators=200, random_state=42), X, y, cv=cv_splitter, scoring="r2")

lr_cv_mae = -cross_val_score(LinearRegression(), X, y, cv=cv_splitter, scoring="neg_mean_absolute_error")
rf_cv_mae = -cross_val_score(RandomForestRegressor(n_estimators=200, random_state=42), X, y, cv=cv_splitter, scoring="neg_mean_absolute_error")

result_table = pd.DataFrame({
    "모델": ["Linear Regression", "Random Forest"],
    "Test MAE": [lr_mae, rf_mae],
    "Test RMSE": [lr_rmse, rf_rmse],
    "Test R²": [lr_r2, rf_r2],
    "CV R² 평균": [lr_cv_r2.mean(), rf_cv_r2.mean()],
    "CV R² 표준편차": [lr_cv_r2.std(), rf_cv_r2.std()],
    "CV MAE 평균": [lr_cv_mae.mean(), rf_cv_mae.mean()],
})
st.dataframe(
    result_table.style.format({
        "Test MAE": "{:.4f}",
        "Test RMSE": "{:.4f}",
        "Test R²": "{:.4f}",
        "CV R² 평균": "{:.4f}",
        "CV R² 표준편차": "{:.4f}",
        "CV MAE 평균": "{:.4f}",
    }),
    hide_index=True,
)

better_model = "Random Forest" if rf_r2 > lr_r2 else "Linear Regression"
st.info(f"Test 데이터 기준 R²가 더 높은 모델: **{better_model}**")

st.divider()

# --- 변수 중요도 ---
st.subheader("변수 중요도 분석")

col1, col2 = st.columns(2)
with col1:
    st.write("선형회귀 - 회귀계수")
    coef_df = pd.DataFrame({
        "변수": FEATURES,
        "계수": lr_model.coef_,
    }).sort_values("계수", key=abs, ascending=False)
    st.bar_chart(coef_df.set_index("변수")["계수"])

with col2:
    st.write("Random Forest - 변수 중요도")
    importance_df = pd.DataFrame({
        "변수": FEATURES,
        "중요도": rf_model.feature_importances_,
    }).sort_values("중요도", ascending=False)
    st.bar_chart(importance_df.set_index("변수")["중요도"])

st.divider()

# --- 사용자 입력 예측 ---
st.subheader("직접 입력해서 OPS 예측하기")
st.caption("아래 11개 기록을 입력하면 두 모델이 예측한 OPS를 보여줍니다.")

input_values = {}
cols = st.columns(3)
defaults = {"타석": 400, "타수": 350, "안타": 90, "2루타": 15, "3루타": 1,
            "홈런": 10, "볼넷": 35, "삼진": 70, "도루": 5, "타점": 45, "득점": 45}

for i, feat in enumerate(FEATURES):
    with cols[i % 3]:
        input_values[feat] = st.number_input(
            feat,
            min_value=0,
            value=defaults[feat],
            step=1,
        )

if st.button("예측 실행"):
    input_df = pd.DataFrame([input_values])[FEATURES]

    lr_result = lr_model.predict(input_df)[0]
    rf_result = rf_model.predict(input_df)[0]

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Linear Regression 예측 OPS", f"{lr_result:.3f}")
    with col2:
        st.metric("Random Forest 예측 OPS", f"{rf_result:.3f}")