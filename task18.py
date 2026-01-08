# Bank Customer Churn Analysis & Prediction

import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

df = pd.read_csv(r"C:\Users\sagar\OneDrive\Desktop\da\bank_churn.csv")
print("Dataset loaded successfully\n")

#  Basic Data
print("Dataset Info:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

#  Churn Distribution (Visualization)
plt.figure()
df['Exited'].value_counts().plot(kind='bar')
plt.title("Customer Churn Distribution")
plt.xlabel("Exited (0 = Stay, 1 = Leave)")
plt.ylabel("Customers")
plt.show()

# Churn by Geography
pd.crosstab(df['Geography'], df['Exited']).plot(kind='bar')
plt.title("Churn by Geography")
plt.xlabel("Country")
plt.ylabel("Customers")
plt.show()

#  Age Distribution of Churned Customer
df[df['Exited'] == 1]['Age'].hist(bins=10)
plt.title("Age of Churned Customers")
plt.xlabel("Age")
plt.ylabel("Customers")
plt.show()

#  Data Preprocessing for ML

# Drop non-useful columns
df = df.drop(['RowNumber', 'CustomerId', 'Surname'], axis=1)

# Encode categorical columns
encoder = LabelEncoder()
for col in ['Geography', 'Gender']:
    df[col] = encoder.fit_transform(df[col])

#  Features & Target
X = df.drop('Exited', axis=1)
y = df['Exited']

#  Train-Test Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train Machine Learning Model
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

#  Model Evaluation
y_pred = model.predict(X_test)

print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

print(" Bank Churn Analysis & Prediction Completed")
