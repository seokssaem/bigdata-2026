# ======================================================================================
# kbo_ops/ops_pipeline/pipeline.py
#
# 전처리 -> 모델 학습 -> 평가를 하나로 묶은 파이프라인
# ======================================================================================

import pandas as pd

from . import config
from . import preprocessing
from . import models
from . import evaluate


def run_pipeline(
    path: str = config.CSV_PATH,
    min_pa: int = config.MIN_PA,
    features: list = config.FEATURES,
    target: str = config.TARGET,
    test_size: float = config.TEST_SIZE,
    cv_folds: int = config.CV_FOLDS,
    random_state: int = config.RANDOM_STATE,
) -> dict:
    """전처리 -> 분할 -> 모델 학습(선형회귀 + RandomForest) -> 평가까지 한 번에 실행한다."""

    # 1. 전처리
    df = preprocessing.preprocess(path, min_pa, features, target)

    # 2. 데이터 분할
    X_train, X_test, y_train, y_test, X, y = models.split_data(
        df, features, target, test_size, random_state
    )
    cv = models.get_cv_splitter(cv_folds, random_state)

    # 3. 모델 학습
    lr = models.train_linear_regression(X_train, y_train)
    rf = models.train_random_forest(X_train, y_train, random_state=random_state)

    # 4. 평가
    lr_result = evaluate.evaluate_model(
        lr, "Linear Regression", X_train, X_test, y_train, y_test, X, y, cv
    )
    rf_result = evaluate.evaluate_model(
        rf, "Random Forest Regressor", X_train, X_test, y_train, y_test, X, y, cv
    )
    results_df = evaluate.compare_models([lr_result, rf_result])

    return {
        "df": df,
        "X_train": X_train, "X_test": X_test, "y_train": y_train, "y_test": y_test,
        "X": X, "y": y,
        "lr": lr, "rf": rf,
        "results_df": results_df,
    }
