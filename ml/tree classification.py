
# Decision Tree Classification Algorithm

import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier, plot_tree
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

# 1. Create dataset
# Features: [Study Hours, Attendance]
X = [
    [1, 50],
    [2, 55],
    [3, 60],
    [4, 65],
    [5, 70],
    [6, 75],
    [7, 80],
    [8, 85],
    [9, 90],
    [10, 95]
]

# 0 = Fail, 1 = Pass
y = [0, 0, 0, 0, 0, 1, 1, 1, 1, 1]

# 2. Split the dataset
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# 3. Create and train the model
model = DecisionTreeClassifier(
    criterion='gini',
    max_depth=3,
    random_state=42
)
model.fit(X_train, y_train)

# 4. Predict test data
y_pred = model.predict(X_test)

print("Actual Values:", y_test)
print("Predicted Values:", y_pred)

# 5. Evaluate the model
print("\nAccuracy:", accuracy_score(y_test, y_pred))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# 6. Predict a new student's result
new_student = [[6, 78]]
prediction = model.predict(new_student)

print("\nStudy Hours:", new_student[0][0])
print("Attendance:", new_student[0][1], "%")
print("Prediction:", "Pass" if prediction[0] == 1 else "Fail")

# 7. Visualize the decision tree
plt.figure(figsize=(12, 7))
plot_tree(
    model,
    feature_names=['Study Hours', 'Attendance'],
    class_names=['Fail', 'Pass'],
    filled=True,
    rounded=True
)
plt.title("Decision Tree Classification")
plt.show()
