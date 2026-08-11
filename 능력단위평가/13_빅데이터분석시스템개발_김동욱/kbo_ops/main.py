
import os

import matplotlib
matplotlib.use("Agg")  # 화면 출력 없이 파일로만 저장 (스크립트 실행 환경용)

from ops_pipeline import config, visualize
from ops_pipeline.pipeline import run_pipeline

RESULTS_DIR = "results"


if __name__ == "__main__":
    os.makedirs(RESULTS_DIR, exist_ok=True)
    visualize.set_korean_font()

    # 1. 파이프라인 실행 (전처리 -> 분할 -> 학습 -> 평가)
    result = run_pipeline()
    df = result["df"]
    X_test, y_test = result["X_test"], result["y_test"]
    lr, rf = result["lr"], result["rf"]
    results_df = result["results_df"]

    print(results_df)
    results_df.to_csv(os.path.join(RESULTS_DIR, "model_comparison.csv"), index=False, encoding="utf-8-sig")

    # 2. 데이터 확인 그래프 저장 (이상치 / 분포 / 상관관계)
    all_cols = config.FEATURES + [config.TARGET]
    visualize.plot_boxplots(df, all_cols, save_path=os.path.join(RESULTS_DIR, "boxplot_check.png"))
    visualize.plot_histograms(df, all_cols, save_path=os.path.join(RESULTS_DIR, "histogram_check.png"))
    visualize.plot_correlation_heatmap(df, all_cols, save_path=os.path.join(RESULTS_DIR, "correlation_heatmap.png"))

    # 3. 모델 결과 그래프 저장 (예측 vs 실제 / 변수 중요도)
    y_pred_lr = lr.predict(X_test)
    y_pred_rf = rf.predict(X_test)
    visualize.plot_prediction_vs_actual(
        y_test,
        {
            "Linear Regression": (y_pred_lr, "#2c7fb8"),
            "Random Forest Regressor": (y_pred_rf, "#e34a33"),
        },
        save_path=os.path.join(RESULTS_DIR, "ops_pred_vs_actual.png"),
    )
    visualize.plot_feature_importance(
        config.FEATURES, rf.feature_importances_, "Random Forest 변수 중요도",
        save_path=os.path.join(RESULTS_DIR, "feature_importance.png"),
    )

    print(f"\n그래프 5개 + 결과표 1개가 '{RESULTS_DIR}/' 폴더에 저장되었습니다.")
