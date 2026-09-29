import streamlit as st
import pandas as pd

# 1. 나만의 자기소개 카드
string1 = st.text_input(
    '이름을 입력하세요',
    placeholder='예)김코딩',
    max_chars=32
)

years = st.slider('경력 연차를 입력하세요',0, 100, 0)

skils = st.multiselect(
    '관심 있는 기술을 모두 선택하세요',
    ['Python', 'SQL', 'Streamlit', 'FastAPI', '머신러닝']
)


st.divider()

st.markdown(f'**이름** : {string1}')
st.markdown(f'**경력** : {years}')
st.markdown(f'**관심 기술** : {",".join(skils)}')