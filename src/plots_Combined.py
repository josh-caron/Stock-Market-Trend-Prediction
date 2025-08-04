import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

def plot_combined(df, window=50):
    df = df.copy()
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()

    # For regression prediction (next day), align prediction to original index
    data = df.copy()
    data['Prev_Close'] = data['Close'].shift(1)
    data = data.dropna().reset_index(drop=True)
    if len(data) < 2:
        print("Not enough data for regression to show combined graph!")
        return

    X = data[['Prev_Close']].values.flatten().reshape(-1,1)
    y = data['Close'].values.flatten()
    model = LinearRegression().fit(X, y)
    reg_preds = model.predict(X)
    # reg_preds aligns with data, which is shorter than df because of .shift and dropna
    # So, pad with NaN for the rows at the start
    reg_full = [np.nan] * (len(df) - len(reg_preds)) + list(reg_preds)

    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price', color='royalblue', linewidth=1)
    valid_sma = ~df[f'SMA_{window}'].isna()
    plt.plot(df['Date'][valid_sma], df[f'SMA_{window}'][valid_sma], label=f'SMA {window}', color='red', linewidth=2.5)
    plt.plot(df['Date'], reg_full, label='Linear Regression Predicted', color='green', linestyle='--', linewidth=2)
    plt.legend()
    plt.title('Actual vs SMA vs Linear Regression')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()
