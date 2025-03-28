import streamlit as st
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.svm import SVR
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import google.generativeai as genai

# Configure Streamlit API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

st.write("📢 Generating synthetic inventory data and saving it as CSV...")

def generate_synthetic_data(samples=1000):
    data = {
        'date': pd.date_range(start='2025-01-01', periods=samples, freq='D'),
        'sales': np.random.randint(50, 500, samples),
        'is_holiday': np.random.choice([0, 1], samples),
        'temperature': np.random.randint(20, 35, samples),
        'customer_trend': np.random.rand(samples) * 10,
    }
    for i in range(1000):
        data[f'feature_{i}'] = np.random.rand(samples) * 100
    df = pd.DataFrame(data)
    df.to_csv("synthetic_inventory_data.csv", index=False)
    return df

# Generate and save synthetic data
df = generate_synthetic_data()
st.write("✅ CSV file 'synthetic_inventory_data.csv' created successfully!")

# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Extract time-based features
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

# Selecting features and target
features = ['day_of_week', 'month', 'year', 'is_holiday', 'temperature', 'customer_trend'] + [f'feature_{i}' for i in range(1000)]
target = 'sales'

# Normalize data
scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])
df[target] = scaler.fit_transform(df[[target]])

# Splitting data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# Linear Regression Model
lr_model = LinearRegression()
lr_model.fit(X_train, y_train)
lr_predictions = lr_model.predict(X_test)

# Random Forest Regressor
rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
rf_model.fit(X_train, y_train)
rf_predictions = rf_model.predict(X_test)

# Gradient Boosting Regressor
gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
gb_model.fit(X_train, y_train)
gb_predictions = gb_model.predict(X_test)

# Support Vector Regressor
svr_model = SVR()
svr_model.fit(X_train, y_train.values.ravel())
svr_predictions = svr_model.predict(X_test)

# Multi-layer Perceptron Regressor (MLP)
mlp_model = MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
mlp_model.fit(X_train, y_train.values.ravel())
mlp_predictions = mlp_model.predict(X_test)

# Evaluate models
def evaluate_model(y_true, y_pred, model_name):
    st.write(f"{model_name} Performance:")
    st.write(f"MAE: {mean_absolute_error(y_true, y_pred)}")
    st.write(f"MSE: {mean_squared_error(y_true, y_pred)}")
    st.write(f"R2 Score: {r2_score(y_true, y_pred)}")
    st.write("\n")

evaluate_model(y_test, lr_predictions, "Linear Regression")
evaluate_model(y_test, rf_predictions, "Random Forest")
evaluate_model(y_test, gb_predictions, "Gradient Boosting")
evaluate_model(y_test, svr_predictions, "Support Vector Machine")
evaluate_model(y_test, mlp_predictions, "Neural Network (MLP)")

# Build LSTM model
X_train_seq = np.reshape(X_train.values, (X_train.shape[0], 1, X_train.shape[1]))
X_test_seq = np.reshape(X_test.values, (X_test.shape[0], 1, X_test.shape[1]))

lstm_model = keras.Sequential([
    keras.layers.LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
    keras.layers.LSTM(50, activation='relu'),
    keras.layers.Dense(1)
])

lstm_model.compile(optimizer='adam', loss='mse')

# Train the LSTM model
lstm_model.fit(X_train_seq, y_train, epochs=20, batch_size=16, validation_data=(X_test_seq, y_test))

# LSTM Predictions
y_pred_lstm = lstm_model.predict(X_test_seq)

# Convert predictions back to original scale
y_test_actual = scaler.inverse_transform(y_test.values.reshape(-1, 1))
y_pred_lstm_actual = scaler.inverse_transform(y_pred_lstm)

# Generate AI Insights
graph_prompt = "Generate detailed insights and recommendations for demand and inventory forecasting based on sales, customer trends, and external factors like holidays and weather. Suggest actionable measures to optimize inventory management."
ai_response = get_ai_response(graph_prompt)
st.write("📊 AI-Generated Insights:", ai_response)

# Plot results
plt.figure(figsize=(12, 6))
plt.plot(y_test_actual, label='Actual Sales', color='blue')
plt.plot(y_pred_lstm_actual, label='Predicted Sales (LSTM)', color='red')
plt.legend()
plt.xlabel('Time')
plt.ylabel('Sales')
plt.title('AI-Powered Demand Forecasting')
st.pyplot(plt)

# Inventory restocking alerts
threshold = 0.3  # Set minimum stock threshold
df['restock_alert'] = df['sales'].apply(lambda x: 'Restock' if x < threshold else 'Sufficient')

# Suggest bulk ordering strategies based on trends
bulk_order_suggestion = "Increase bulk orders" if y_pred_lstm_actual.mean() > y_test_actual.mean() else "Optimize stock levels"
st.write("📦 Suggested Inventory Strategy:", bulk_order_suggestion)
