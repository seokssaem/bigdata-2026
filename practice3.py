import streamlit as st

string1 = st.text_input(
    '이름을 입력하세요',
    placeholder="",
    max_chars=32
)

string2 = st.multiselect(
    '관심 분야를 선택하세요',
    ['빅데이터', '웹개발', '클라우드', 'AI', '보안']
)

string3 = st.slider('이번 수업 만족도를 선택하세요(0~10)',0, 10, 5)

st.divider()

if st.button('제출하기'):
    st.success('제출이 완료되었습니다. 참여해주셔서 감사합니다.')
    st.markdown(f'**응답자**: {string1}')
    st.markdown(f'**관심분야**: {",".join(string2)}')
    st.markdown(f'**만족도**: {string3}/10')