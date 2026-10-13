
# Data Loading, Cleaning, Missing Values, and Visualization

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Create a sample dataset
data = {
    'Name': ['Ravi', 'Sita', 'John', 'Priya', 'Ravi'],
    'Age': [20, 21, np.nan, 22, 20],
    'Marks': [85, 90, 78, np.nan, 85],
    'Department': ['CSE', 'ECE', 'CSE', 'IT', 'CSE']
}

df = pd.DataFrame(data)

# 2. Data Loading
print("Original Dataset:")
print(df)

# 3. Data Cleaning
# Remove duplicate rows
df = df.drop_duplicates()

print("\nDataset after removing duplicates:")
print(df)

# 4. Handling Missing Values
print("\nMissing Values:")
print(df.isnull().sum())

# Fill missing numerical values with their column mean
df['Age'] = df['Age'].fillna(df['Age'].mean())
df['Marks'] = df['Marks'].fillna(df['Marks'].mean())

print("\nDataset after handling missing values:")
print(df)

# 5. Data Visualization

# Bar chart of student marks
plt.figure(figsize=(8, 5))
plt.bar(df['Name'], df['Marks'])
plt.xlabel('Student Name')
plt.ylabel('Marks')
plt.title('Student Marks')
plt.show()

# Histogram of ages
plt.figure(figsize=(8, 5))
plt.hist(df['Age'], bins=5, edgecolor='black')
plt.xlabel('Age')
plt.ylabel('Frequency')
plt.title('Age Distribution')
plt.show()

# Heatmap of numerical data
plt.figure(figsize=(6, 4))
sns.heatmap(
    df[['Age', 'Marks']].corr(),
    annot=True,
    cmap='coolwarm'
)
plt.title('Correlation Heatmap')
plt.show()

print("\nData preprocessing and visualization completed.")
