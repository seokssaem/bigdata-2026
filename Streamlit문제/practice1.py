import streamlit as st

st.title("나만의 자기소개 카드")
name = st.text_input(
    '이름을 입력하세요.',
    placeholder='예)김코딩',
    max_chars=12
)

years = st.slider("경력 연차를 선택하세요", 0, 10, 0)

skill = st.multiselect(
    "관심 있는 기술을 모두 선택하세요",
    ["Python", "SQL", "Streamlit", "FastAPI", "머신러닝"]
)

st.divider()

if name:
    with st.container():
        col1, col2 = st.columns([1, 4])
        with col1:
            first_char = name[0] if len(name) > 0 else ""
            st.markdown(
                f"""
                <div style="
                    background-color: lightblue;
                    color: black;
                    width: 60px;
                    height: 60px;
                    border-radius: 50%;
                    display: flex;
                    align-items: center;
                    justify-content: center;">
                    {first_char}
                </div>
                """,
                unsafe_allow_html=True
            )
            
        with col2:
            st.write(f"**이름:** {name}")
            st.write(f"**경력 연차:** {years}년")
            skill_str = ", ".join(skill) if skill else "없음"
            st.write(f"**관심 기술:** {skill_str}")

else:
    st.info("이름을 입력하면 카드가 생성됩니다.")