import math
import streamlit as st
import matplotlib.pyplot as plt
from data_loader import load_batter

plt.rcParams["font.family"] = "Malgun Gothic"
plt.rcParams["axes.unicode_minus"] = False

st.title("히스토그램 분석")

df = load_batter()

# 선택 가능한 변수 22개
VARIABLES = [
    "타석", "타수", "안타", "2루타", "3루타", "홈런", "볼넷", "삼진", "도루", "타점", "득점", "OPS",
    "타율", "출루율", "장타율",
    "WAR", "wRC+", "BABIP", "순수장타율", "GPA", "삼진비율",
]

min_pa_only = st.checkbox("100타석 이상만 분석에 포함")
analysis_df = df[df["타석"] >= 100] if min_pa_only else df

st.caption(f"분석 대상: {len(analysis_df):,}명 (전체 {len(df):,}명 중)")

st.divider()

st.write("히스토그램으로 볼 변수 선택 (복수 선택 가능)")
selected_vars = st.pills(
    "변수 선택",
    options=VARIABLES,
    selection_mode="multi",
    default=["OPS"],
    label_visibility="collapsed",
)

if not selected_vars:
    st.info("위에서 변수를 하나 이상 선택해주세요.")
else:
    n = len(selected_vars)
    n_cols = min(4, n)
    n_rows = math.ceil(n / n_cols)

    fig, axes = plt.subplots(n_rows, n_cols, figsize=(4 * n_cols, 3.2 * n_rows))
    axes = axes.flatten() if hasattr(axes, "flatten") else [axes]

    for i, var in enumerate(selected_vars):
        ax = axes[i]
        data = analysis_df[var].dropna()
        skewness = data.skew()
        ax.hist(data, bins=20, color="#1f77b4")
        ax.set_title(f"{var} (왜도={skewness:.2f})")

    for j in range(n, len(axes)):
        axes[j].axis("off")

    fig.tight_layout()
    st.pyplot(fig, use_container_width=False)