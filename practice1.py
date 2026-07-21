import streamlit as st

st.title('나만의 자기소개 카드')
name = st.text_input(
    '이름을 입력하세요',
    placeholder='예) 김코딩',
    max_chars=32
)

year = st.slider(
    '경력 연차를 선택하세요',
    min_value=0,
    value=0
)

tech = st.multiselect(
    '관심 있는 기술을 모두 선택하세요',
    ['Python', 'SQL', 'Streamlit', 'FastAPI', '머신러닝']
)

st.divider()

if name:
    st.text(f'이름: {name}')
    st.text(f'경력 연차: {year}')
    st.text(f'관심 기술: {", ".join(tech)}')
else:
    st.write('이름을 입력하면 카드가 생성됩니다.')