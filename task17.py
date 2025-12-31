import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load Titanic dataset
df = sns.load_dataset("titanic")

# 1. Survival Rate by Class (Matplotlib)
df_pclass = df.dropna(subset=['pclass'])

survival_by_class = df_pclass.groupby('pclass')['survived'].mean()

plt.figure()
plt.bar(survival_by_class.index, survival_by_class.values)
plt.xlabel("Passenger Class")
plt.ylabel("Survival Rate")
plt.title("Survival Rate by Passenger Class")
plt.show()


# 2. Gender Survival Count (Seaborn)
plt.figure()
sns.countplot(
    x='sex',
    hue='survived',
    data=df,
    order=['male', 'female'],
    palette=sns.color_palette("pastel")
)
plt.title("Survival Count by Gender")
plt.show()


# 3. Age Distribution Histogram
df['Age_filled'] = df['age'].fillna(df['age'].median())

plt.figure()
plt.hist(df['Age_filled'], bins=20, alpha=0.5, label="All Passengers")
plt.hist(
    df[df['survived'] == 1]['Age_filled'],
    bins=20,
    alpha=0.7,
    color='red',
    label="Survivors"
)
plt.xlabel("Age")
plt.ylabel("Count")
plt.title("Age Distribution (with Survivors Overlay)")
plt.legend()
plt.show()


# 4. Embarked vs Survival (Pointplot)
df['embarked'] = df['embarked'].fillna('S')

plt.figure()
sns.pointplot(
    x='embarked',
    y='survived',
    data=df,
    ci=68
)
plt.title("Survival Rate by Embarkation Port")
plt.show()


# 5. Fare vs Survival (Scatter Plot)
colors = df['survived'].map({0: 'red', 1: 'green'})

plt.figure()
plt.scatter(df['fare'], df['survived'], c=colors, alpha=0.6)
plt.ylim(-0.1, 1.1)
plt.xlabel("Fare")
plt.ylabel("Survived")
plt.title("Fare vs Survival")
plt.xlim(0, df['fare'].quantile(0.99))  # handle outliers
plt.show()


# 6. Cabin Class vs Survival (Catplot)
sns.catplot(
    x='pclass',
    y='survived',
    hue='sex',
    kind='bar',
    data=df
)
plt.suptitle("Survival by Passenger Class and Gender", y=1.03)
plt.show()



# 7. Age vs Survival (Violin Plot)
df['survived_label'] = df['survived'].map({0: 'No', 1: 'Yes'})

plt.figure()
sns.violinplot(
    x='survived_label',
    y='age',
    data=df,
    inner='quartiles'
)
plt.title("Age Distribution by Survival")
plt.show()


# 8. Correlation Heatmap
corr = df[['age', 'fare', 'pclass', 'survived']].corr()

plt.figure()
sns.heatmap(
    corr,
    annot=True,
    cmap='viridis'
)
plt.title("Correlation Heatmap")
plt.show()


# 9. Family Size vs Survival
df['FamilySize'] = df['sibsp'] + df['parch'] + 1

# Grouped bar (correct approach)
family_group = df.groupby(['FamilySize', 'survived']).size().unstack()

family_group.plot(kind='bar')
plt.xlabel("Family Size")
plt.ylabel("Passenger Count")
plt.title("Survival Count by Family Size")
plt.show()

# Optional: survival rate version (better insight)
df.groupby('FamilySize')['survived'].mean().plot(kind='bar')
plt.xlabel("Family Size")
plt.ylabel("Survival Rate")
plt.title("Survival Rate by Family Size")
plt.show()

