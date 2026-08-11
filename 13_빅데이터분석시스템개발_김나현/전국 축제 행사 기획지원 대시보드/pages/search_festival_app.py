"""
search_festival_app.py

작업일자: 2026-08-03
작업자: 장호균
목적: 축제명, 개최장소 분석을 위한 파일
데이터 파일: 13_bigdata_streamlit/전국문화축제정보정리_raw.csv

실행:
streamlit run search_festival_app.py
"""
from pathlib import Path
import joblib
import pandas as pd
import streamlit as st

# 상위 폴더에 있는 공용 모델 파일 경로 설정
DATA_PATH = Path(__file__).resolve().parent.parent /'input'/'전국문화축제정보정리_raw.csv'

# 타이틀 및 안내
st.title('전국 문화축제 행사 및 개최장소 검색 툴')
st.caption('데이터 파일에 등록된 실제 전국 축제 정보를 검색하고 벤치마킹 장소를 찾아보세요')

df = None
encodings_to_try = ['utf-8-sig', 'cp949', 'utf-8']

for encoding in encodings_to_try:
    try:
        df = pd.read_csv(DATA_PATH, encoding=encoding)
        # 성공적으로 읽어왔다면 반복문을 탈출합니다.
        break
    except UnicodeDecodeError:
        # 에러가 나면 다음 인코딩 방식으로 넘어가서 다시 시도합니다.
        continue
    except FileNotFoundError:
        st.error("❌ '전국문화축제정보정리_raw.csv' 파일을 찾을 수 없습니다. 파일이 상위 폴더에 있는지 확인해 주세요.")
        st.stop()

# 사용자가 검색하기 편하게 데이터 컬럼 이름 확인 안내
st.sidebar.markdown("### 📊 데이터 구조 확인")
st.sidebar.write("현재 파일에 포함된 정보 종류:")
st.sidebar.caption(", ".join(df.columns))

# st.markdown("---")

# 검색창 UI 구성
st.subheader("✍️ 찾고 싶은 축제 키워드나 장소를 입력하세요")
col1, col2 = st.columns(2)

with col1:
    search_name = st.text_input("🎪 축제명 검색 (예: 치맥, 불꽃, 문화)", value="")
with col2:
    search_place = st.text_input("📍 개최장소/지역 검색 (예: 대구, 서울, 부산)", value="")

# 검색 로직 실행 (사용자가 글자를 입력하면 실시간 필터링)
filtered_df = df.copy()

# 축제명 컬럼이 존재할 때 검색어 필터링 (대소문자 구분 없음)
name_column = '축제명' if '축제명' in df.columns else df.columns[0] 
place_column = '개최장소' if '개최장소' in df.columns else (df.columns[1] if len(df.columns) > 1 else df.columns[0])

if search_name:
    # 입력한 단어가 포함된 행만 남기기
    filtered_df = filtered_df[filtered_df[name_column].astype(str).str.contains(search_name, case=False, na=False)]

if search_place:
    # 입력한 장소 단어가 포함된 행만 남기기
    filtered_df = filtered_df[filtered_df[place_column].astype(str).str.contains(search_place, case=False, na=False)]


# 최종 결과 화면에 표 출력
st.markdown("---")
st.subheader(f"📊 검색 결과 (총 {len(filtered_df)}건 발견)")

if len(filtered_df) > 0:
    st.dataframe(filtered_df, width='stretch')
    
    # [가장 간단한 구조] '행사기간' 열의 평균을 구해서 소수점 1자리까지 보여줍니다.
    # 💡 만약 본인 엑셀 파일의 정확한 열 이름이 '행사기간'이 아니라면 아래 글자만 바꾸시면 됩니다!
    avg_duration = filtered_df['행사기간'].mean()
    st.info(f"💡 **기획 데이터 팁:** 검색된 축제들의 평균 행사기간은 약 **{avg_duration:.1f}일** 수준입니다.")

else:
    st.warning("🔍 입력하신 조건과 일치하는 축제 정보가 데이터 파일에 없습니다. 다른 단어로 검색해 보세요.")
