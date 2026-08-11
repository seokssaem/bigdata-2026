# ======================================================================================
# kbo_ops/ops_pipeline/preprocessing.py
#
# 데이터 로드 & 전처리
# ======================================================================================
import pandas as pd

from . import config


def load_data(path: str = config.CSV_PATH) -> pd.DataFrame:
    """CSV 파일을 읽어온다."""
    df = pd.read_csv(path, encoding="utf-8-sig")
    return df


def filter_min_pa(df: pd.DataFrame, min_pa: int = config.MIN_PA) -> pd.DataFrame:
    """표본 신뢰도 확보를 위해 최소 타석 이상인 선수만 남긴다."""
    return df[df["타석"] >= min_pa].reset_index(drop=True)


def select_columns(
    df: pd.DataFrame,
    features: list = config.FEATURES,
    target: str = config.TARGET,
) -> pd.DataFrame:
    """분석에 필요한 컬럼만 선택한다."""
    keep_cols = ["선수", "팀"] + features + [target]
    return df[keep_cols].copy()


def check_missing(df: pd.DataFrame) -> pd.Series:
    """컬럼별 결측치 개수를 반환한다."""
    return df.isna().sum()


def preprocess(
    path: str = config.CSV_PATH,
    min_pa: int = config.MIN_PA,
    features: list = config.FEATURES,
    target: str = config.TARGET,
) -> pd.DataFrame:
    """전처리 파이프라인: 로드 -> 필터링 -> 컬럼 선택"""
    df = load_data(path)
    df = filter_min_pa(df, min_pa)
    df = select_columns(df, features, target)
    return df
