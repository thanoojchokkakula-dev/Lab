
# Logistic Regression for Binary Classification

import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Create dataset
X = np.array([
    [1], [2], [3], [4], [5],
    [6], [7], [8], [9], [10]
])

# 0 = Fail, 1 = Pass
y = np.array([0, 0, 0, 0, 0, 1, 1, 1, 1, 1])

# 2. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.3, random_state=42, stratify=y
)

# 3. Create and train the model
model = LogisticRegression()
model.fit(X_train, y_train)

# 4. Predict classes
y_pred = model.predict(X_test)

print("Actual Values:", y_test)
print("Predicted Values:", y_pred)

# 5. Evaluate the model
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 6. Predict for a new input
hours = np.array([[7]])
prediction = model.predict(hours)
probability = model.predict_proba(hours)

print("\nHours Studied:", hours[0][0])
print("Predicted Class:", "Pass" if prediction[0] == 1 else "Fail")
print("Probability of Passing:", probability[0][1])

# 7. Visualize the results
plt.scatter(X, y, color='blue', label='Actual Data')

x_values = np.linspace(1, 10, 200).reshape(-1, 1)
y_prob = model.predict_proba(x_values)[:, 1]

plt.plot(x_values, y_prob, color='red', label='Logistic Curve')
plt.axhline(0.5, color='green', linestyle='--', label='Decision Threshold')
plt.xlabel('Hours Studied')
plt.ylabel('Probability of Passing')
plt.title('Logistic Regression - Binary Classification')
plt.legend()
plt.show()
