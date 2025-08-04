import time
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import os

def train_and_predict(df):
    """
    Train on first 80% and plot predictions vs. actual on last 20%.
    """
    os.makedirs('plots', exist_ok=True)
    data = df.copy()
    data['Prev_Close'] = data['Close'].shift(1)
    data = data.dropna().reset_index(drop=True)
    if len(data) < 2:
        print("Not enough data for regression!")
        return
    X = data[['Prev_Close']].values.flatten().reshape(-1,1)
    y = data['Close'].values.flatten()
    split = int(0.8 * len(data))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    model = LinearRegression().fit(X_train, y_train)
    preds = model.predict(X_test)
    mse = mean_squared_error(y_test, preds) if len(y_test) else float('nan')
    print(f"Mean Squared Error: {mse:.4f}")
    if len(y_test):
        plt.figure(figsize=(12, 6))
        plt.plot(data['Date'][split:], y_test, label='Actual')
        plt.plot(data['Date'][split:], preds, label='Predicted')
        plt.legend()
        plt.title('Linear Regression Prediction')
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig('plots/lr_plot.png')
        plt.show()
        plt.close()

def regression_signal(df):
    """
    Compute next-day prediction and BUY/SELL signal for the last data point.
    """
    data = df.copy()
    data['Prev_Close'] = data['Close'].shift(1)
    data = data.dropna().reset_index(drop=True)
    if len(data) < 2:
        return {"predicted": None, "current": None, "signal": "Not enough data for regression", "slope": None, "intercept": None}
    X = data[['Prev_Close']].values.flatten().reshape(-1,1)
    y = data['Close'].values.flatten()
    model = LinearRegression().fit(X, y)
    last_prev = float(X[-1][0])
    predicted = float(model.predict([[last_prev]])[0])
    current = float(y[-1])
    signal = "BUY (Predicted > Current)" if predicted > current else "SELL (Predicted < Current)"
    return {"predicted": predicted, "current": current, "signal": signal,
            "slope": float(model.coef_[0]), "intercept": float(model.intercept_)}

def evaluate_regression(df):
    """
    Evaluate Linear Regression strategy similarly to SMA:
      - Accuracy, ROI, Duration
    """
    start = time.time()
    data = df.copy()
    data['Prev_Close'] = data['Close'].shift(1)
    data = data.dropna().reset_index(drop=True)
    if len(data) < 2:
        return {"accuracy": 0.0, "roi": 0.0, "duration": 0.0}
    X = data[['Prev_Close']].values.flatten().reshape(-1,1)
    y = data['Close'].values.flatten()
    split = int(0.8 * len(data))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]
    if len(X_test) == 0:
        return {"accuracy": 0.0, "roi": 0.0, "duration": 0.0}
    model = LinearRegression().fit(X_train, y_train)
    preds = model.predict(X_test)
    duration = time.time() - start
    signals = preds > X_test[:, 0]
    actual_up = y_test > X_test[:, 0]
    accuracy = np.mean(signals == actual_up) * 100 if len(signals) > 0 else 0.0
    profit = (y_test - X_test[:, 0])[signals].sum() if np.any(signals) else 0.0
    trades = X_test[:, 0][signals] if np.any(signals) else np.array([])
    roi = (profit / trades.sum()) * 100 if trades.sum() else 0.0
    return {"accuracy": accuracy, "roi": roi, "duration": duration}
