'''
Festival/pages_src/data_loader.py

작성일 : 26-08-11
작성자 : 1조 - 김시현, 김나현, 장호균
목적 : 여러 페이지에서 공통으로 사용하는 'csv불러오기' 함수를 한 곳에 모아둔 파일

'''
import streamlit as st
import pandas as pd

MONTH_ORDER = [f'{i}월' for i in range(1, 13)]

@st.cache_data
def load_festival(path: str='./input/전국문화축제정보정리_raw.csv') -> pd.DataFrame:
    """
    전국문화축제정보정리_raw.csv를 읽어 반환한다. (전국 문화축제 정보 데이터)
    """
    dtype_map = {
        '축제명': 'category',
        '개최장소': 'category',
        '주관기관명': 'category',
        '제공기관명': 'category',
        '지하철유무': 'category',
        '광역시도': 'category'
    }

    df = pd.read_csv(path, dtype=dtype_map)

    if '버스정류장수' in df.columns:
        df['버스정류장수'] = pd.to_numeric(df['버스정류장수'], errors='coerce').fillna(0).astype('int64')

    else:
        st.warning('-')
    
    df['축제시작일자'] = pd.to_datetime(df['축제시작일자'])
    df['축제종료일자'] = pd.to_datetime(df['축제종료일자'])

    if '개최월' in df.columns:
        if df['개최월'].dtype not in ['object', 'category'] or not df['개최월'].astype(str).str.contains('월').any:
            df['개최월'] = df['개최월'].astype(str).str.split('.').str[0] + '월'
    else:
        df['개최월'] = df['축제시작일자'].dt.month.astype(str) + '월'

    df['개최월'] = pd.Categorical(df['개최월'], categories=MONTH_ORDER, ordered=True)
    return df