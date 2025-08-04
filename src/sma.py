import matplotlib.pyplot as plt
import time
import numpy as np
import pandas as pd
import os

def compute_sma(df, window=50):
    os.makedirs('plots', exist_ok=True)
    df = df.copy()
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    plt.figure(figsize=(12, 6))
    # Plot Close in blue
    plt.plot(df['Date'], df['Close'], label='Close Price', color='royalblue', linewidth=1)
    # Plot SMA in thick red
    valid = ~df[f'SMA_{window}'].isna()
    plt.plot(df['Date'][valid], df[f'SMA_{window}'][valid], label=f'SMA {window}', color='red', linewidth=3)
    plt.legend()
    plt.title(f'Simple Moving Average ({window}-day)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/sma_plot.png')
    plt.show()
    plt.close()

def sma_signal(df, window=50):
    df = df.copy()
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    current_price = df['Close'].iloc[-1].item()
    current_sma = df[f'SMA_{window}'].iloc[-1].item()
    if pd.isna(current_sma):
        signal = "Not enough data for SMA"
    else:
        signal = "BUY (Price > SMA)" if current_price > current_sma else "SELL (Price < SMA)"
    return {"current": current_price, "sma": current_sma if not pd.isna(current_sma) else None, "signal": signal}

def evaluate_sma(df, window=50):
    start = time.time()
    data = df.copy()
    data['SMA'] = data['Close'].rolling(window=window).mean()
    data = data.dropna().reset_index(drop=True)

    prices = data['Close'].values.flatten()
    sma = data['SMA'].values.flatten()
    signals = prices > sma
    if len(prices) < 2:
        return {"accuracy": 0.0, "roi": 0.0, "duration": 0.0}
    next_prices = prices[1:]
    prices = prices[:-1]
    signals = signals[:-1]
    actual_up = next_prices > prices

    accuracy = (signals == actual_up).mean() * 100 if len(signals) > 0 else 0.0
    profit = (next_prices - prices)[signals].sum() if np.any(signals) else 0.0
    trades = prices[signals] if np.any(signals) else np.array([])
    roi = (profit / trades.sum()) * 100 if trades.sum() else 0.0
    duration = time.time() - start
    return {"accuracy": accuracy, "roi": roi, "duration": duration}
#