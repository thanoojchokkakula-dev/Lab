
# Gradient Descent Algorithm

import numpy as np
import matplotlib.pyplot as plt

# 1. Create dataset
X = np.array([1, 2, 3, 4, 5], dtype=float)
y = np.array([2, 4, 6, 8, 10], dtype=float)

# 2. Initialize parameters
m = 0.0          # Slope
b = 0.0          # Intercept
learning_rate = 0.01
epochs = 1000
n = len(X)

cost_history = []

# 3. Perform Gradient Descent
for i in range(epochs):
    y_pred = m * X + b

    # Calculate gradients
    dm = (-2 / n) * np.sum(X * (y - y_pred))
    db = (-2 / n) * np.sum(y - y_pred)

    # Update parameters
    m = m - learning_rate * dm
    b = b - learning_rate * db

    # Calculate Mean Squared Error
    y_pred = m * X + b
    cost = np.mean((y - y_pred) ** 2)
    cost_history.append(cost)

# 4. Display optimized parameters
print("Optimized Slope (m):", round(m, 4))
print("Optimized Intercept (b):", round(b, 4))
print("Final Cost (MSE):", round(cost_history[-1], 6))

# 5. Predict new value
x_new = 6
prediction = m * x_new + b
print("Prediction for X = 6:", round(prediction, 2))

# 6. Visualize regression line
plt.scatter(X, y, color='blue', label='Actual Data')
plt.plot(X, m * X + b, color='red', label='Gradient Descent Line')
plt.xlabel('X')
plt.ylabel('Y')
plt.title('Gradient Descent Regression')
plt.legend()
plt.show()

# 7. Visualize cost reduction
plt.plot(range(epochs), cost_history)
plt.xlabel('Epoch')
plt.ylabel('Mean Squared Error')
plt.title('Cost Reduction During Gradient Descent')
plt.show()
