'''
Festival/pages_src/search.py

작성일 : 26-08-11
작성자 :  1조 - 김시현, 김나현, 장호균
목적 : 폼 안에 입력 위젯들(축제명, 광역시도, 기간, 버스정류장 수, 지하철유무) 조건들을 조작할 때마다
        재실행되지 않고 "검색"버튼을 누르는 순간에만 한 번에 처리되도록 폼을 사용

        만약에 데이터가 많을 때 폼 없이 위젯을 조작하면 필터링을 다시 하면 체감 속도가
        느려진다. --> st.form을 사용한다.

'''
import pandas as pd
import streamlit as st
from data_loader import load_festival

st.title('🔎 문화축제 검색 - st.form 위젯 사용')

df = load_festival()

with st.form('fastival_search_form'):
    col1, col2 = st.columns(2)
    with col1:
        keyword = st.text_input('축제명 검색 (일부만 입력 가능, 비워두면 전체)')
    with col2:
        all_regions = ['전체'] + df['광역시도'].dropna().unique().sort_values().tolist()
        region_pick = st.selectbox('광역시도 선택', all_regions)

    date_range = st.date_input(
        '축제 개최 기간 (시작일 기준)',
        value=(df['축제시작일자'].min(), df['축제시작일자'].max()),
        min_value=df['축제시작일자'].min(),
        max_value=df['축제시작일자'].max(),
    )

    if '버스정류장' in df.columns:
        min_bus = int(df['버스정류장수'].min())
        max_bus = int(df['버스정류장수'].max())
        if min_bus == max_bus:
            max_bus = max_bus + 1
    else:
        min_bus, max_bus = 0, 10
    # bus_range = st.slider(
    #     '인근 버스정류장 수 범위',
    #     min_value=min_bus,
    #     max_value=max_bus,
    #     value=(min_bus, max_bus)
    # )

    subway_option = st.selectbox('지하철 연계 유무', ['전체', '유(Y)', '무(N)'])

    submitted = st.form_submit_button('🔎 축제 검색 실행!')

# 버튼을 눌렀다면!
if submitted:
    filterd = df.copy()

    if keyword:
        filterd = filterd[filterd['축제명'].str.contains(keyword, na=True)]

    if region_pick != '전체':
        filterd = filterd[filterd['광역시도'] == region_pick]

    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start, end = date_range
        filterd = filterd[
            (filterd['축제시작일자'] >= pd.to_datetime(start)) &
            (filterd['축제시작일자'] <= pd.to_datetime(end))
        ]

    # filterd = filterd[
    #     (filterd['버스정류장수'] >= bus_range[0]) &
    #     (filterd['버스정류장수'] <= bus_range[1])
    # ]

    if subway_option == '유(Y)':
        filterd = filterd[filterd['지하철유무'].isin(['Y', '유'])]
    elif subway_option == '무(N)':
        filterd = filterd[filterd['지하철유무'].isin(['N', '무'])]

    st.session_state.last_search_result = filterd

    st.write(f'검색 결과 : {len(filterd):,}건')

    base_cols = ['축제명', '광역시도', '개최장소', '축제시작일자', '축제종료일자',
                 '주관기관명', '방문객수', '버스정류장수', '지하철유무', '전화번호']
    display_cols = [col for col in base_cols if col in filterd.columns]

    st.dataframe(
        filterd
        .sort_values('축제시작일자', ascending=True)
        .head(500)[display_cols]
    )

    if len(filterd) > 500:
        st.caption(f'''표에는 최신 축제 상위 500건만 표시됩니다.
                    전체 {len(filterd):,}건은 아래 버튼으로 다운로드 하세요.''')

    csv_bytes = filterd.to_csv(index=True).encode('utf-8-sig')
    st.download_button(
        '검색 결과 축제 리스트 CSV 다운로드',
        data=csv_bytes,
        file_name='festival_search_result.csv',
        mime='text/csv',
    )