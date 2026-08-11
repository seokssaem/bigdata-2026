'''
Festival/pages_src/trend.py

작성일 : 26-08-11
작성자 : 1조 - 김시현, 김나현, 장호균
목적 : 전체 축제 기준으로 "일별 방문객 추이"와 "대중교통 인프라(지하철/버스)별 패턴"을 함께 보여주는 페이지

'''
import streamlit as st
from data_loader import load_festival

st.title('📊 기간 및 대중교통 인프라 추이 분석')

df = load_festival()

infra_type = st.radio(
    '교통 접근성 기준 선택',
    ['전체 축제', '지하철 연계 축제만(Y)', '인근 버스정류장 다수(5개 이상)'],
    horizontal=True
)

if infra_type == '지하철 연계 축제만(Y)':
    filtered = df[df['지하철유무'].isin(['Y', '유'])]
elif infra_type == '인근 버스정류장 다수(5개 이상)':
    filtered = df[df['버스정류장수'] >= 5]
else:
    filtered = df.copy()

st.subheader('📆 축제 시작일 기준 일별 방문객 추이')
daily_total = filtered.groupby('축제시작일자')['방문객수'].sum()
st.line_chart(daily_total)

st.subheader('🗺️ 광역시도별 평균 축제 방문객 수')
region_avg = filtered.groupby('광역시도', observed=True)['방문객수'].mean().sort_values(ascending=False)
st.bar_chart(region_avg)

st.subheader('🎪 주요 축제별 방문객 직접 비교')
top_festivals = (
    df.groupby('축제명', observed=True)['방문객수']
    .sum()
    .nlargest(20)
    .index.tolist()
)

compare_festivals = st.multiselect(
    '비교할 축제 선택 (총 방문객수 상위 20개 축제 중 최대 5개 권장)',
    options=top_festivals,
    default=top_festivals[:3],
)

if compare_festivals:
    compare_df = df[df['축제명'].isin(compare_festivals)]
    pivot = compare_df.pivot_table(index='축제시작일자', columns='축제명', values='방문객수', aggfunc='sum')
    st.line_chart(pivot)

st.session_state.last_viewed_ride_type = infra_type