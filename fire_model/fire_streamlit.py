from pathlib import Path
import json
import pandas as pd
import streamlit as st

METRICS_PATH = Path(__file__).resolve().parent / 'metrics.json'

st.set_page_config(page_title='실습: 화재 인명피해 모델 성능', page_icon='📊')

st.title('📊화재 인명피해 예측 모델')

if not METRICS_PATH.exists():
    st.error('metrics.json 파일이 없습니다. 터미널에서 `python fire.py`를 먼저 실행하세요')
    st.stop()

with open(METRICS_PATH, encoding='utf-8-sig') as f:
    metrics = json.load(f)

col1, col2, col3, col4 = st.columns(4)
col1.metric('테스트 샘플 수', f"{metrics['test_rows']:,}")
col2.metric('ROC-AUC', f"{metrics['roc_auc']:.3f}")
col3.metric('재현율(Recall)', f"{metrics['recall_casualty']:.1%}")
col4.metric('정밀도(Precision)', f"{metrics['precision_casualty']:.1%}")

st.caption(f"판정 기준(threshold) = {metrics['threshold']} · F1-score = {metrics['f1_casualty']:.3f}")

st.divider()

st.subheader('변수 중요도 (그룹별 합산)')
importance = metrics['feature_importance_grouped']
importance_df = pd.DataFrame({
    '변수': list(importance.keys()),
    '중요도': list(importance.values())
}).sort_values('중요도', ascending=False).set_index('변수')
st.bar_chart(importance_df)

st.divider()

st.subheader('세부 피처 중요도 Top 10')
top_df = pd.DataFrame(metrics['top_features'])
top_df.columns = ['원본 변수', '세부 피처', '중요도']
st.dataframe(top_df, use_container_width=True, hide_index=True)