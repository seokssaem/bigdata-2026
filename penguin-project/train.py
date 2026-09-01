import pandas as pd 
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
import joblib

def train_model():
    df = pd.read_csv('penguins.csv')

    df = df.dropna(subset=['species'])
    
    features = ['bill_length_mm', 'bill_depth_mm', 'flipper_length_mm', 'body_mass_g']
    for col in features:
        df[col] = df[col].fillna(df[col].mean())

    X = df[features]
    y = df['species']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f'모델 검증 정확도: {acc:.4f}')

    # 🎯 파일명을 'penguin_model.pkl'로 저장합니다.
    joblib.dump(model, 'penguin_model.pkl')
    print("💾 모델 저장 완료: penguin_model.pkl")

if __name__ == '__main__':
    train_model()