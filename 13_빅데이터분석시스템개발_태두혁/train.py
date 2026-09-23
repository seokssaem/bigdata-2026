# 라이브러리 불러오기
from pathlib import Path
import json
import joblib  
import pandas as pd
from sklearn.compose import ColumnTransformer 
from sklearn.ensemble import RandomForestClassifier 
from sklearn.impute import SimpleImputer  
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

HERE = Path(__file__).resolve().parent
DATA_PATH = HERE/'fire.csv'

MODEL_PATH = HERE/'casualty_model.joblib'
METRICS_PATH = HERE/'metrics.json'

FEATURES = ['시도', '발화요인소분류', '장소대분류', '발생_월', '발생_시간', '발생_요일']
TARGET = '인명피해_발생여부'

NUMERIC = ['발생_월', '발생_시간', '발생_요일']
CATEGORICAL = ['시도', '발화요인소분류', '장소대분류']

def build_pipeline() -> Pipeline:
    """전처리와 모델 하나로 묶어 학습"""
    numeric_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler())
    ])

    category_pipe = Pipeline([
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer([
        ('category', category_pipe, CATEGORICAL),
        ('numeric', numeric_pipe, NUMERIC)
    ])  

    model = RandomForestClassifier(
        n_estimators=300,
        class_weight='balanced',
        random_state=42,
        min_samples_leaf=10,
        n_jobs=-1,
        verbose=1
    )

    return Pipeline([('preprocess', preprocessor), ('model', model)])

def train() -> dict:
    """모델 학습 및 평가 지표 반환"""
    data = pd.read_csv(DATA_PATH)

    X = data[FEATURES]
    y = data[TARGET]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.25, stratify=y, random_state=42
    )

    pipeline = build_pipeline()
    pipeline.fit(X_train, y_train)

    probabilities = pipeline.predict_proba(X_test)[:, 1]

    THRESHOLD = 0.3
    predictions = (probabilities >= THRESHOLD).astype(int)

    report = classification_report(y_test, predictions, output_dict=True, zero_division=0)

    # 보고용 핵심 지표
    metrics = {
        'test_rows':len(X_test),
        'threshold':THRESHOLD,
        'roc_auc':round(float(roc_auc_score(y_test, probabilities)), 4),
        'recall_casualty':round(float(report['1']['recall']), 4),
        'precision_casualty':round(float(report['1']['precision']), 4),
        'f1_casualty':round(float(report['1']['f1-score']), 4),
        'confusion_matrix':confusion_matrix(y_test, predictions).tolist()
    }

    # 변수 중요도 확인
    # .named_steps : Pipeline의 속성 / 리스트로 정의한 단계들을 이름으로 꺼낼 수 있게 해준다
    # .named_transformers_ : ColumnTransformer의 속성 / 정의한 변환기들을 이름으로 꺼낼 수 있게 해준다
    ohe = pipeline.named_steps['preprocess'].named_transformers_['category'].named_steps['onehot']
    # 컬럼 순서 → 원핫 된 범주형 컬럼 + 수치형 컬럼
    feature_names = list(ohe.get_feature_names_out(CATEGORICAL)) + NUMERIC
    # 랜덤포레스트 모델에서 feature_importances_ 꺼내기 / 컬럼 순서가 feature_names과 일치
    importances = pipeline.named_steps['model'].feature_importances_
    imp_df = pd.DataFrame({'feature':feature_names, 'importance':importances})

    # 범주형 변수는 원핫 인코딩으로 여러 컬럼(시도_서울, 시도_부산...)으로 쪼개지면서
    # 컬럼 하나에 중요도가 몰리는 수치형 변수보다 개별 중요도가 작게 나뉘어 보이는 착시가 생긴다
    def base_feature(name: str) -> str:
        """원핫 인코딩된 컬럼명 → 원본 범주형 변수명"""
        for col in CATEGORICAL:
            if name.startswith(col+'_'):
                return col
        return name

    imp_df['base_feature'] = imp_df['feature'].apply(base_feature)

    # 원본 변수 단위로 재집계한 중요도
    grouped_importance = (
        imp_df.groupby('base_feature')['importance']
        .sum()
        .sort_values(ascending=False)
        .round(4)
    )
    metrics['feature_importance_grouped'] = grouped_importance.to_dict()

    # group_importance(그룹 순위) -> importance(그룹 내 개별 순위) 순으로 정렬
    imp_df['group_importance'] = imp_df['base_feature'].map(grouped_importance)
    top_features = imp_df.sort_values(
        ['group_importance', 'importance'],
        ascending=False
    ).head(10)
    # .to_dict(orient='records') : 데이터프레임을 json으로 저장 가능
    metrics['top_features'] = top_features.round(4)[['base_feature', 'feature', 'importance']].to_dict(orient='records')

    joblib.dump(pipeline, MODEL_PATH)

    METRICS_PATH.write_text(json.dumps(metrics, ensure_ascii=False, indent=2), encoding='utf-8-sig')

    return metrics

if __name__ == '__main__':
    print(json.dumps(train(), ensure_ascii=False, indent=2))