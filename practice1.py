import streamlit as st

st.title('나만의 자기소개 카드')

name = st.text_input(
    '이름',
    placeholder='이름을 입력하시오')

score = st.slider(
    '경력',
    0,10)

tech = st.multiselect(
    '관심있는 기술을 모두 선택하세요',
    ['IT','반도체','금융','AI','연구','Python','SQL']
)
st.divider()

col1, col2 = st.columns(2)
if name is not '':
    with col1:
        st.text('col1')
    with col2:
        st.write(f"**이름** : {name}")
        st.write(f'**경력** : {score}년')
        st.write(f'**관심 기술** : {", ".join(tech)}')
else:
    custom_css = """
    <style>
    /* st.code 박스 전체와 내부 pre, code 태그 배경색 변경 */
    .stCode, .stCode pre, .stCode code {
        background-color: #E0F7FA; /* 밝은 하늘색 */
        color: #01579B;           
    }
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)
    st.code('이름을 입력하면 카드가 생성됩니다.','text')