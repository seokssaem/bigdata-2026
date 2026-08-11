# ======================================================================================
# kbo_ops/ops_pipeline/visualize.py
#
# 시각화 함수
# ======================================================================================
import platform

import numpy as np
import pandas as pd
from scipy import stats
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import seaborn as sns
from sklearn.metrics import r2_score


def set_korean_font():
    """OS별 한글 폰트를 자동으로 찾아 설정 (없으면 경고만 출력)"""
    system = platform.system()
    candidates = {
        "Windows": ["Malgun Gothic"],
        "Darwin": ["AppleGothic"],
        "Linux": ["NanumGothic", "Noto Sans CJK KR", "Noto Sans CJK JP"],
    }.get(system, [])

    available = {f.name for f in fm.fontManager.ttflist}
    for name in candidates:
        if name in available:
            plt.rcParams["font.family"] = name
            break
    else:
        print("경고: 한글 폰트를 찾지 못했습니다. 그래프의 한글이 깨질 수 있습니다.")
    plt.rcParams["axes.unicode_minus"] = False


def plot_boxplots(df: pd.DataFrame, columns: list, save_path: str = None):
    n = len(columns)
    ncols = 4
    nrows = -(-n // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 4 * nrows))
    axes = axes.flatten()

    for i, col in enumerate(columns):
        axes[i].boxplot(df[col], vert=True)
        axes[i].set_title(col)
    for j in range(n, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_histograms(df: pd.DataFrame, columns: list, save_path: str = None):
    n = len(columns)
    ncols = 4
    nrows = -(-n // ncols)
    fig, axes = plt.subplots(nrows, ncols, figsize=(16, 4 * nrows))
    axes = axes.flatten()

    for i, col in enumerate(columns):
        axes[i].hist(df[col], bins=20, color="#2c7fb8", edgecolor="white")
        skew = stats.skew(df[col])
        axes[i].set_title(f"{col} (왜도={skew:.2f})")
    for j in range(n, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_correlation_heatmap(df: pd.DataFrame, columns: list, save_path: str = None):
    corr = df[columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", center=0, ax=ax)
    ax.set_title("독립변수-OPS 상관관계 히트맵")
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig, corr


def plot_prediction_vs_actual(y_test, predictions: dict, save_path: str = None):
    """predictions: {"모델이름": (y_pred, color)}"""
    n = len(predictions)
    fig, axes = plt.subplots(1, n, figsize=(6.5 * n, 5.5))
    if n == 1:
        axes = [axes]

    for ax, (name, (y_pred, color)) in zip(axes, predictions.items()):
        ax.scatter(y_test, y_pred, alpha=0.6, color=color, edgecolor="white", s=45)
        lims = [y_test.min() - 0.02, y_test.max() + 0.02]
        ax.plot(lims, lims, color="gray", linestyle="--", linewidth=2, label="완벽 예측선 (y=x)")
        ax.set_xlabel("실제 OPS")
        ax.set_ylabel("예측 OPS")
        r2_val = r2_score(y_test, y_pred)
        ax.set_title(f"{name} (R²={r2_val:.3f})")
        ax.legend()

    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig


def plot_feature_importance(features: list, importances, title: str, save_path: str = None):
    imp_df = pd.DataFrame({"변수": features, "중요도": importances}).sort_values("중요도", ascending=False)

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.barh(imp_df["변수"], imp_df["중요도"], color="#e34a33")
    ax.invert_yaxis()
    ax.set_xlabel("중요도")
    ax.set_title(title)
    plt.tight_layout()
    if save_path:
        plt.savefig(save_path, dpi=150, bbox_inches="tight")
    return fig, imp_df
