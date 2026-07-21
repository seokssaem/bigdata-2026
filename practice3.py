# =============================================================
# ~/bigdata202/fastapi//Streamlit/practice3.py
#
#  Streamlit 라이브러리 기초 연습문제 / 실행 할 때 터미널 streamlit run [파일명] 
#
# ===========================================================
import streamlit as st

st.title('간단 설문 & 만족도 조사')

string1 = st.text_input(
    '이름을 입력하세요', 
    placeholder='예) 홍길동', 
    max_chars=25
)

skill = st.multiselect(
    "관심 있는 분야를 선택하세요", 
    ['빅데이터', '웹개발', '클라우드', 'AI', '보안']
)

score = st.slider('이번 수업 만족도를 선택하세요 (0~10)', 0, 10, 5)

if st.button('제출하기', type='secondary'):
    
    st.success('제출이 완료되었습니다. 참여해주셔서 감사합니다.')
    st.write("")
    
    st.write(f"**응답자:** {string1}")
    selected_skills = ", ".join(skill)
    st.write(f"**관심 분야:** {selected_skills}")
    st.write(f"**만족도:** {score} / 10")