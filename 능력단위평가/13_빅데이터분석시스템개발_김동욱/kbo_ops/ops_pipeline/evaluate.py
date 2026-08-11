# ======================================================================================
# kbo_ops/ops_pipeline/evaluate.py
#
# 모델 성능 평가
# ======================================================================================
import numpy as np
import pandas as pd
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def evaluate_test(model, X_test, y_test) -> dict:
    """Test 데이터로 MAE, RMSE, R2를 계산한다."""
    y_pred = model.predict(X_test)
    return {
        "Test MAE": mean_absolute_error(y_test, y_pred),
        "Test RMSE": np.sqrt(mean_squared_error(y_test, y_pred)),
        "Test R2": r2_score(y_test, y_pred),
    }


def evaluate_cv(model, X, y, cv) -> dict:
    """K-Fold 교차검증으로 R2, MAE 평균/표준편차를 계산한다."""
    cv_r2 = cross_val_score(model, X, y, cv=cv, scoring="r2")
    cv_mae = -cross_val_score(model, X, y, cv=cv, scoring="neg_mean_absolute_error")
    return {
        "CV R2 평균": cv_r2.mean(),
        "CV R2 표준편차": cv_r2.std(),
        "CV MAE 평균": cv_mae.mean(),
    }


def evaluate_model(model, model_name: str, X_train, X_test, y_train, y_test, X, y, cv) -> dict:
    """Test 평가 + 교차검증을 합쳐서 하나의 결과 딕셔너리로 반환한다."""
    result = {"모델": model_name}
    result.update({k: round(v, 4) for k, v in evaluate_test(model, X_test, y_test).items()})
    result.update({k: round(v, 4) for k, v in evaluate_cv(model, X, y, cv).items()})
    return result


def compare_models(results: list) -> pd.DataFrame:
    """여러 모델의 평가 결과를 하나의 표로 정리한다."""
    return pd.DataFrame(results)
