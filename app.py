import streamlit as st
import google.generativeai as genai
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

# ✅ Configure API Key securely
if "GOOGLE_API_KEY" in st.secrets:
    api_key = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=api_key)
else:
    st.error("⚠️ API Key is missing. Go to Streamlit Cloud → Settings → Secrets and add your API key.")
    st.stop()

# ✅ AI Response Generator
def get_ai_response(prompt, fallback_message="⚠️ AI response unavailable. Please try again later."):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content(prompt)
        return response.text.strip() if hasattr(response, "text") and response.text.strip() else fallback_message
    except Exception as e:
        return f"⚠️ AI Error: {str(e)}\n{fallback_message}"

# ✅ Generate Synthetic Data
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

# ✅ Data Preprocessing
df['date'] = pd.to_datetime(df['date'])
df['day_of_week'] = df['date'].dt.dayofweek
df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

features = ['day_of_week', 'month', 'year', 'is_holiday', 'temperature', 'customer_trend'] + [f'feature_{i}' for i in range(1000)]
target = 'sales'

scaler = MinMaxScaler()
df[features] = scaler.fit_transform(df[features])
df[target] = scaler.fit_transform(df[[target]])

X_train, X_test, y_train, y_test = train_test_split(df[features], df[target], test_size=0.2, random_state=42)

# ✅ Machine Learning Models
models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=100, random_state=42),
    "Gradient Boosting": GradientBoostingRegressor(n_estimators=100, random_state=42),
    "Support Vector Regressor": SVR(),
    "Neural Network (MLP)": MLPRegressor(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
}

predictions = {}
for name, model in models.items():
    model.fit(X_train, y_train.values.ravel())
    predictions[name] = model.predict(X_test)

# ✅ Evaluate Models
def evaluate_model(y_true, y_pred, model_name):
    return {
        "MAE": mean_absolute_error(y_true, y_pred),
        "MSE": mean_squared_error(y_true, y_pred),
        "R2 Score": r2_score(y_true, y_pred)
    }

evaluations = {name: evaluate_model(y_test, pred, name) for name, pred in predictions.items()}
st.write("### Model Performance")
st.write(evaluations)

# ✅ Build LSTM Model
X_train_seq = np.reshape(X_train.values, (X_train.shape[0], 1, X_train.shape[1]))
X_test_seq = np.reshape(X_test.values, (X_test.shape[0], 1, X_test.shape[1]))

lstm_model = keras.Sequential([
    keras.layers.LSTM(50, activation='relu', return_sequences=True, input_shape=(X_train_seq.shape[1], X_train_seq.shape[2])),
    keras.layers.LSTM(50, activation='relu'),
    keras.layers.Dense(1)
])

lstm_model.compile(optimizer='adam', loss='mse')
lstm_model.fit(X_train_seq, y_train, epochs=20, batch_size=16, validation_data=(X_test_seq, y_test))

y_pred_lstm = lstm_model.predict(X_test_seq)
y_test_actual = scaler.inverse_transform(y_test.values.reshape(-1, 1))
y_pred_lstm_actual = scaler.inverse_transform(y_pred_lstm)

# ✅ Plot Results
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(y_test_actual, label='Actual Sales', color='blue')
ax.plot(y_pred_lstm_actual, label='Predicted Sales (LSTM)', color='red')
ax.legend()
ax.set_xlabel('Time')
ax.set_ylabel('Sales')
ax.set_title('AI-Powered Demand Forecasting')
st.pyplot(fig)

# ✅ Inventory Restocking Alerts
df['restock_alert'] = df['sales'].apply(lambda x: 'Restock' if x < 0.3 else 'Sufficient')

# ✅ AI-Driven Inventory Strategy
bulk_order_suggestion = "Increase bulk orders" if y_pred_lstm_actual.mean() > y_test_actual.mean() else "Optimize stock levels"
st.write("### Suggested Inventory Strategy:", bulk_order_suggestion)
