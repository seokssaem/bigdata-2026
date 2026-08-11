import streamlit as st
import pandas as pd

@st.cache_data
def load_batter(path: str="./files/hitter.csv") -> pd.DataFrame:
    """
    hitter.csv를 읽어 반환한다. (2025년 KBO 타자 기록)
    """
    dtype_map = {        
        "선수": "category",
        "팀": "category",
    }
    df = pd.read_csv(path, dtype=dtype_map)

    return df