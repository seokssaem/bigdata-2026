import streamlit as st

st.title('간단 설문 & 만족도 조사')

name = st.text_input('이름을 입력하세요', max_chars=32)

field = st.multiselect(
    '관심 있는 분야를 선택하세요',
    ['빅데이터', '웹개발', '클라우드', 'AI', '보안']
)

satisfaction = st.slider(
    '이번 수업 만족도를 선택하세요(0~10)',
    min_value=0,
    max_value=10,
    value=5
)

st.divider()

submit = st.button('제출하기', type='secondary')

if submit:
    st.write('제출이 완료되었습니다. 참여해주셔서 감사합니다.')
    st.text(f'응답자: {name}')
    st.text(f'관심 분야: {", ".join(field)}')
    st.text(f'만족도: {satisfaction}/10')