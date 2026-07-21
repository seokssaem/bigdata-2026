import streamlit as st

st.title("간단 설문 & 만족도 조사")
name = st.text_input(
    '이름을 입력하세요.', max_chars=12
)

skill = st.multiselect(
    "관심 있는 분야를 선택하세요",
    ["빅데이터", "웹개발", "클라우드", "AI", "보안"]
)

score = st.slider("이번 수업 만족도를 선택하세요(0~10)", 0, 10, 0)

st.divider()

if st.button("제출하기"):
    st.success("제출이 완료되었습니다. 참여해주셔서 감사합니다.")
    st.write(f"**응답자:** {name}")
    st.write(f"**관심 분야:** {', '.join(skill)}")
    st.write(f"**만족도:** {score} / 10")