import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use("ggplot")

# Load Titanic dataset
df = sns.load_dataset("titanic")
df.columns = df.columns.str.lower()


# Basic inspection
print(df.head())
print(df.isnull().sum())
print(df.info())
# 1. Survival Rate by Class
survival_by_class = df.groupby("pclass")["survived"].mean()
print("\nSurvival Rate by Class:\n", survival_by_class)

# 2. Gender Bias
gender_survival = df.groupby("sex")["survived"].agg(["mean", "count"])
overall_survival = df["survived"].mean()

print("\nGender Survival:\n", gender_survival)
print("Overall survival rate:", overall_survival)

# 3. Missing Cabin Analysis
df["has_cabin"] = df["deck"].notna()

cabin_analysis = df.groupby("has_cabin")["survived"].agg(["count", "mean"])
print("\nCabin Analysis:\n", cabin_analysis)

# 4. Family Size Impact
df["family_size"] = df["sibsp"] + df["parch"] + 1

print("\nFamily size correlation:")
print(df[["family_size", "survived"]].corr())

df["family_size"].hist(bins=10)
plt.title("Family Size Distribution")
plt.xlabel("Family Size")
plt.ylabel("Count")
plt.show()

# 5. Age Distribution

df["age"] = df["age"].fillna(df["age"].median())

df[df["survived"] == 1]["age"].plot(kind="hist", bins=30, alpha=0.6, label="Survived")
df[df["survived"] == 0]["age"].plot(kind="hist", bins=30, alpha=0.6, label="Not Survived")

plt.legend()
plt.xlabel("Age")
plt.title("Age Distribution by Survival")
plt.show()

# 6. Embarkation Analysis
df["embark_town"] = df["embark_town"].fillna(df["embark_town"].mode()[0])

embark_survival = df.groupby("embark_town")["survived"].mean()
print("\nEmbarkation Survival Rate:\n", embark_survival)

# 7. Ticket Prefix Analysis 
if "ticket" in df.columns:
    df["ticket_prefix"] = df["ticket"].astype(str).str.extract(r"([A-Za-z]+)")
    df["ticket_prefix"] = df["ticket_prefix"].fillna("NUM")

    ticket_survival = df.groupby("ticket_prefix")["survived"].mean()
    print("\nTicket Prefix Survival:\n", ticket_survival)
else:
    print("\nTicket column not present — skipped.")


# 8. Missing Fare Handling
print("\nMissing Fare:", df["fare"].isnull().sum())

df["fare"] = df.groupby("pclass")["fare"].transform(
    lambda x: x.fillna(x.median())
)

print("\nMedian Fare by Class:\n", df.groupby("pclass")["fare"].median())

# 9. Correlation Matrix
corr = df[["age", "fare", "survived"]].corr()
print("\nCorrelation Matrix:\n", corr)

sns.heatmap(corr, annot=True, cmap="coolwarm")
plt.title("Correlation Matrix")
plt.show()

# 10. Advanced Family Groups
df["family_only"] = df["sibsp"] + df["parch"]

df["family_group"] = df["family_only"].apply(
    lambda x: "Solo" if x == 0 else ("Small Family" if x >= 2 else "Pair")
)

family_survival = df.groupby("family_group")["survived"].mean()
print("\nFamily Group Survival:\n", family_survival)
