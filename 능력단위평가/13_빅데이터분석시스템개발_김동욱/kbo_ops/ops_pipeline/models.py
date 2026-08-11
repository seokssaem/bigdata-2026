# ======================================================================================
# kbo_ops/ops_pipeline/models.py
#
# 데이터 분할 & 모델 학습
# ======================================================================================
import pandas as pd
from sklearn.model_selection import train_test_split, KFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor

from . import config


def split_data(
    df: pd.DataFrame,
    features: list = config.FEATURES,
    target: str = config.TARGET,
    test_size: float = config.TEST_SIZE,
    random_state: int = config.RANDOM_STATE,
):
    """지도학습(회귀)을 위한 Train/Test 분할"""
    X = df[features]
    y = df[target]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )
    return X_train, X_test, y_train, y_test, X, y


def get_cv_splitter(n_splits: int = config.CV_FOLDS, random_state: int = config.RANDOM_STATE) -> KFold:
    """교차검증용 KFold 객체 생성"""
    return KFold(n_splits=n_splits, shuffle=True, random_state=random_state)


def train_linear_regression(X_train, y_train) -> LinearRegression:
    """선형회귀 모델 학습"""
    model = LinearRegression()
    model.fit(X_train, y_train)
    return model


def train_random_forest(
    X_train, y_train, n_estimators: int = 200, random_state: int = config.RANDOM_STATE
) -> RandomForestRegressor:
    """Random Forest Regressor 모델 학습"""
    model = RandomForestRegressor(n_estimators=n_estimators, random_state=random_state)
    model.fit(X_train, y_train)
    return model
