import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error

# 1. Load Data
df = pd.read_csv(r'C:\Users\sagar\OneDrive\Desktop\da\hospital_readmissions.csv')

# 2. Preprocessing
# Split 'blood_pressure' (e.g., "130/72") into two numeric columns
df[['sys_bp', 'dia_bp']] = df['blood_pressure'].str.split('/', expand=True).astype(float)

# Drop non-numeric/ID columns and the classification label
df_ml = df.drop(columns=['patient_id', 'blood_pressure', 'readmitted_30_days'])

# Convert categorical text (Gender, Diabetes, etc.) into numeric binary columns
df_ml = pd.get_dummies(df_ml, drop_first=True)

# 3. Define Features (X) and Target (y)
X = df_ml.drop(columns=['length_of_stay'])
y = df_ml['length_of_stay']

# 4. Split and Scale
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# 5. Apply Regression Models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=10),
    "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
}

print("--- Regression Performance ---")
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    print(f"{name} -> R2: {r2:.4f}, MSE: {mse:.4f}")

# 6. Visualization (using the best performing model)
best_model = LinearRegression().fit(X_train_scaled, y_train)
y_pred_final = best_model.predict(X_test_scaled)

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_final, alpha=0.2, color='blue', label='Predictions')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2, label='Perfect Prediction')
plt.title('Actual vs Predicted Length of Stay')
plt.xlabel('Actual Days')
plt.ylabel('Predicted Days')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()