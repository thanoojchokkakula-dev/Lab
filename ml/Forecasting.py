
# Time-Series Analysis and Forecasting using ARIMA

import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

# 1. Create time-series dataset
data = {
    'Month': pd.date_range(
        start='2025-01-01', periods=24, freq='MS'
    ),
    'Sales': [
        100, 110, 108, 120, 125, 130,
        128, 140, 145, 150, 148, 160,
        165, 170, 168, 180, 185, 190,
        188, 200, 205, 210, 208, 220
    ]
}

df = pd.DataFrame(data)
df.set_index('Month', inplace=True)

# 2. Display dataset
print("Time-Series Data:")
print(df)

# 3. Visualize historical data
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Sales'], marker='o')
plt.title('Monthly Sales Trend')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.grid(True)
plt.show()

# 4. Split into training and testing data
train = df['Sales'][:-4]
test = df['Sales'][-4:]

# 5. Build and train ARIMA model
model = ARIMA(train, order=(1, 1, 1))
model_fit = model.fit()

# 6. Forecast test-period values
predictions = model_fit.forecast(steps=len(test))

print("\nActual Sales:")
print(test.values)

print("\nForecast Sales:")
print(predictions.values)

# 7. Evaluate the forecast
print("\nMean Absolute Error:",
      round(mean_absolute_error(test, predictions), 2))

print("Mean Squared Error:",
      round(mean_squared_error(test, predictions), 2))

# 8. Forecast the next 6 months
final_model = ARIMA(df['Sales'], order=(1, 1, 1))
final_fit = final_model.fit()
future = final_fit.forecast(steps=6)

future_dates = pd.date_range(
    start=df.index[-1] + pd.offsets.MonthBegin(1),
    periods=6,
    freq='MS'
)

forecast_df = pd.DataFrame(
    {'Forecast Sales': future.values},
    index=future_dates
)

print("\nNext 6 Months Forecast:")
print(forecast_df)

# 9. Plot actual and forecast values
plt.figure(figsize=(10, 5))
plt.plot(df.index, df['Sales'], label='Historical Sales')
plt.plot(
    future_dates, future.values,
    marker='o', linestyle='--', color='red',
    label='Forecast Sales'
)
plt.title('Time-Series Sales Forecast')
plt.xlabel('Month')
plt.ylabel('Sales')
plt.legend()
plt.grid(True)
plt.show()
