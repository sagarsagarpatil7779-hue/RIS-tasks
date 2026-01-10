import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

# Note: Handle XGBoost if it is not installed in your environment
try:
    from xgboost import XGBRegressor
    has_xgboost = True
except ImportError:
    has_xgboost = False

# 1. Load dataset
df = pd.read_csv('possum.csv')

features = ['skullw', 'totlngth', 'footlgth', 'belly', 'chest', 'eye', 'age']
X = df[features]
y = df['hdlngth']

# 2. Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 3. Handle missing values
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# 4. Scaling
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Define Models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=100),
    "Lasso Regression": Lasso(alpha=0.01),
    "Random Forest": RandomForestRegressor(
        random_state=42,
        max_features='sqrt'
    )
}

if has_xgboost:
    models["XGBoost"] = XGBRegressor(
        n_estimators=30,
        max_depth=5,
        learning_rate=0.1,
        gamma=1,
        random_state=42
    )

# Lists to capture results for plotting
model_names = []
test_r2_scores = []
best_model_name = ""
best_r2 = -float('inf')
best_y_pred = None

# 6. Train and Evaluate
for name, model in models.items():
    model.fit(X_train_scaled, y_train)

    y_train_pred = model.predict(X_train_scaled)
    y_test_pred = model.predict(X_test_scaled)

    test_r2 = r2_score(y_test, y_test_pred)
    
    # Store results for plots
    model_names.append(name)
    test_r2_scores.append(test_r2)

    print(f"{name}")
    print(f"Train R2: {r2_score(y_train, y_train_pred):.4f}")
    print(f"Test  R2: {test_r2:.4f}")
    print(f"MSE     : {mean_squared_error(y_test, y_test_pred):.4f}")
    print("=" * 50)

    # Identify the best model for the scatter plot
    if test_r2 > best_r2:
        best_r2 = test_r2
        best_model_name = name
        best_y_pred = y_test_pred


# Plot 1: Bar Chart Comparison of R2 Scores
plt.figure(figsize=(10, 6))
sns.barplot(x=model_names, y=test_r2_scores, palette='viridis')
plt.title('Comparison of Test R2 Scores Across Models', fontsize=14)
plt.ylabel('R2 Score')
plt.ylim(0, 1) # R2 usually falls between 0 and 1
plt.xticks(rotation=15)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.savefig('model_comparison_r2.png')
plt.show()

# Plot 2: Actual vs Predicted for the Best Model (Random Forest)
plt.figure(figsize=(10, 6))
plt.scatter(y_test, best_y_pred, alpha=0.7, color='teal', edgecolors='k')
# Red dashed line represents perfect prediction
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.title(f'Actual vs Predicted Head Length ({best_model_name})', fontsize=14)
plt.xlabel('Actual Head Length')
plt.ylabel('Predicted Head Length')
plt.grid(True, linestyle='--', alpha=0.6)
plt.tight_layout()
plt.savefig('best_model_actual_vs_predicted.png')
plt.show()

print("\nSuccess: Plots generated and saved as 'model_comparison_r2.png' and 'best_model_actual_vs_predicted.png'")