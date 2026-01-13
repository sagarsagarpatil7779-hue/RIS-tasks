import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor

# 1. Load the dataset
df = pd.read_csv(r'C:\Users\sagar\OneDrive\Desktop\da\hospital_readmissions.csv')

# 2. Data Cleaning & Feature 
# Split the 'blood_pressure' string into two numeric columns
df[['sys_bp', 'dia_bp']] = df['blood_pressure'].str.split('/', expand=True).astype(float)

# Drop irrelevant columns and classification target
df_ml = df.drop(columns=['patient_id', 'blood_pressure', 'readmitted_30_days'])

# Convert categorical variables into numeric dummy variables
df_encoded = pd.get_dummies(df_ml, drop_first=True)

# 3. Define Features (X) and Target (y)
X = df_encoded.drop(columns=['length_of_stay'])
y = df_encoded['length_of_stay']

# 4. Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. Handling Missing Values & Scaling
imputer = SimpleImputer(strategy='mean')
scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(imputer.fit_transform(X_train))
X_test_scaled = scaler.transform(imputer.transform(X_test))

# 6. Define Regression Models
models = {
    "Linear Regression": LinearRegression(),
    "Ridge Regression": Ridge(alpha=10),
    "Lasso Regression": Lasso(alpha=0.01),
    "Random Forest": RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
}

# Results storage
model_names = []
r2_results = []
best_r2 = -np.inf
best_model_name = ""
best_y_pred = None

# 7. Train and Evaluate
print("--- Hospital Readmissions: Regression Analysis (Dark Mode) ---")
for name, model in models.items():
    model.fit(X_train_scaled, y_train)
    y_pred = model.predict(X_test_scaled)
    
    r2 = r2_score(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    
    model_names.append(name)
    r2_results.append(r2)
    
    print(f"{name:20} | R2 Score: {r2:7.4f} | MSE: {mse:.4f}")
    
    if r2 > best_r2:
        best_r2 = r2
        best_model_name = name
        best_y_pred = y_pred

#  8. Plotting Code (Black Background) 

# Apply the dark theme style
plt.style.use('dark_background')

# Plot 1: Model Comparison (R2 Score)
plt.figure(figsize=(10, 6), facecolor='black')
ax = sns.barplot(x=model_names, y=r2_results, palette='magma')
plt.title('Comparison of Regression Model Accuracy (R2)', fontsize=14, color='white')
plt.ylabel('R-Squared Score', color='white')
plt.xticks(rotation=15, color='white')
plt.yticks(color='white')
plt.grid(axis='y', linestyle='--', alpha=0.3)
plt.tight_layout()
plt.savefig('hosp_model_comparison_black.png', facecolor='black')
plt.show()

# Plot 2: Actual vs Predicted (Best Model)
plt.figure(figsize=(10, 6), facecolor='black')
# Plotting a subset for better visibility
plt.scatter(y_test[:500], best_y_pred[:500], alpha=0.6, color='cyan', edgecolors='white', label='Predicted vs Actual')
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], color='orange', linestyle='--', lw=2, label='Perfect Fit')
plt.title(f'Actual vs Predicted Length of Stay ({best_model_name})', fontsize=14, color='white')
plt.xlabel('Actual Days in Hospital', color='white')
plt.ylabel('Predicted Days', color='white')
plt.legend()
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('hosp_actual_vs_predicted_black.png', facecolor='black')
plt.show()

print(f"\nCompleted! Plots saved as 'hosp_model_comparison_black.png' and 'hosp_actual_vs_predicted_black.png'")
