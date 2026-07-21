import streamlit as st

st.title('간단 설문 & 만족도 조사')

name = st.text_input(
    '이름을 입력하세요'
)
tech = st.multiselect(
    '관심 있는 분야를 선택하세요',
    ['빅데이터','SQL','Python','java','C','AI']
)
score = st.slider(
    '이번 수업 만족도를 선택하세요 (0~10)',
    0,10   
)

st.divider()
if st.button('제출하기',key='bt1'):
    custom_css = """
    <style>
    /* st.code 박스 전체와 내부 pre, code 태그 배경색 변경 */
    .stCode, .stCode pre, .stCode code {
        background-color: #98FB98; /* 밝은 초록색 */
        color: green;           
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.code("제출이 완료되었습니다. 참여해주셔서 감사합니다.", language="text")

    st.write(f'**응답자**: {name}')
    st.write(f'**관심분야**: {", ".join(tech)}')
    st.write(f'**만족도**: {score}/10')