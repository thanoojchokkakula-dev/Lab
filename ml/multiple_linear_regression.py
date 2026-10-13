
# Multiple Linear Regression

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score

# 1. Create dataset
data = {
    'Area': [1000, 1500, 1800, 2000, 2200, 2500, 2800, 3000, 3200, 3500],
    'Bedrooms': [2, 3, 3, 4, 3, 4, 4, 5, 4, 5],
    'Age': [10, 5, 8, 3, 6, 2, 4, 1, 3, 2],
    'Price': [20, 30, 35, 40, 42, 50, 55, 60, 65, 70]
}

df = pd.DataFrame(data)

print("Dataset:")
print(df)

# 2. Select input features and target
X = df[['Area', 'Bedrooms', 'Age']]
y = df['Price']

# 3. Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# 4. Create and train the model
model = LinearRegression()
model.fit(X_train, y_train)

# 5. Predict values
y_pred = model.predict(X_test)

print("\nActual Prices:", y_test.values)
print("Predicted Prices:", y_pred)

# 6. Evaluate the model
print("\nMean Squared Error:", mean_squared_error(y_test, y_pred))
print("R2 Score:", r2_score(y_test, y_pred))

# 7. Predict the price of a new house
new_house = pd.DataFrame({
    'Area': [2400],
    'Bedrooms': [3],
    'Age': [5]
})

predicted_price = model.predict(new_house)
print("\nPredicted Price of New House:", predicted_price[0], "lakhs")

# 8. Visualize actual vs predicted prices
plt.scatter(y_test, y_pred, color='blue')
plt.plot([y.min(), y.max()], [y.min(), y.max()], color='red')
plt.xlabel('Actual Price (Lakhs)')
plt.ylabel('Predicted Price (Lakhs)')
plt.title('Actual vs Predicted House Prices')
plt.show()
