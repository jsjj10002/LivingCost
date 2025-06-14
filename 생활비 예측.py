import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 데이터 불러오기
df = pd.read_csv('통합데이터_세종제거.csv')

# 수치형으로 변환 (문자열 → NaN)
df = df.apply(pd.to_numeric, errors='coerce')

# 결측치 비율이 40% 이상인 열 제거
threshold = 0.4
df = df.loc[:, df.isnull().mean() < threshold]

# 결측치 있는 행 제거
df.dropna(inplace=True)

# 타깃 컬럼 지정
target_col = '인당소비_민간소비지출액(천원)'
if target_col not in df.columns:
    raise KeyError(f"{target_col} 컬럼이 존재하지 않습니다.")

# 특성과 타깃 분리
X = df.drop(columns=[target_col])
y = df[target_col]

# 데이터 정규화
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 학습/테스트 분리
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# 모델 정의 및 학습
models = {
    "선형 회귀": LinearRegression(),
    "랜덤 포레스트": RandomForestRegressor(random_state=42)
}

results = []
for name, model in models.items():
    model.fit(X_train, y_train)
    preds = model.predict(X_test)
    mae = mean_absolute_error(y_test, preds)
    mse = mean_squared_error(y_test, preds)
    rmse = np.sqrt(mse)
    results.append((name, round(mae, 2), round(rmse, 2)))

# 결과 출력
results_df = pd.DataFrame(results, columns=["모델", "MAE", "RMSE"])
print(results_df)
