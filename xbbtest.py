import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import r2_score, mean_squared_error
import seaborn as sns

# 한글 폰트 설정
plt.rcParams["font.family"] = "Malgun Gothic"  # 윈도우 기준
plt.rcParams["axes.unicode_minus"] = False

# 데이터 불러오기
df = pd.read_csv("통합데이터_출처정리완료.csv", encoding="utf-8")

# 타겟 및 피처 선택
target_col = "인당소득_1인당 민간소비"
X = df.drop(columns=[target_col])
y = df[target_col]

# 숫자형 컬럼만 선택 (선형 회귀 및 결정 트리에서 NaN, 문자형 에러 방지)
X = X.select_dtypes(include=[np.number]).dropna(axis=1)
y = y.astype(float)

# 학습/테스트 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 모델 학습
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_preds = lr_model.predict(X_test)

tree_model = DecisionTreeRegressor(max_depth=5, random_state=42)
tree_model.fit(X_train, y_train)
tree_preds = tree_model.predict(X_test)

# 평가지표 출력
lr_rmse = np.sqrt(mean_squared_error(y_test, lr_preds))
tree_rmse = np.sqrt(mean_squared_error(y_test, tree_preds))

print(f"[선형 회귀] R²: {r2_score(y_test, lr_preds):.4f}, RMSE: {lr_rmse:.2f}")
print(f"[결정 트리] R²: {r2_score(y_test, tree_preds):.4f}, RMSE: {tree_rmse:.2f}")

# 결과 저장
results_df = pd.DataFrame({
    "모델": ["선형 회귀", "결정 트리"],
    "R²": [r2_score(y_test, lr_preds), r2_score(y_test, tree_preds)],
    "RMSE": [lr_rmse, tree_rmse]
})
results_df.to_csv("모델_성능_평가_결과.csv", index=False, encoding="utf-8-sig")

# 변수 중요도 시각화 및 저장
# 선형 회귀 계수
coef_df = pd.DataFrame({
    "변수": X.columns,
    "회귀계수": lr_model.coef_
}).sort_values(by="회귀계수", key=np.abs, ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=coef_df.head(10), x="회귀계수", y="변수", palette="coolwarm")
plt.title("선형 회귀: 가장 영향력 있는 변수 (상위 10개)")
plt.tight_layout()
plt.savefig("선형회귀_변수중요도.png")
plt.close()

# 결정 트리 중요도
imp_df = pd.DataFrame({
    "변수": X.columns,
    "중요도": tree_model.feature_importances_
}).sort_values(by="중요도", ascending=False)

plt.figure(figsize=(10, 6))
sns.barplot(data=imp_df.head(10), x="중요도", y="변수", palette="YlGnBu")
plt.title("결정 트리: 가장 영향력 있는 변수 (상위 10개)")
plt.tight_layout()
plt.savefig("결정트리_변수중요도.png")
plt.close()
