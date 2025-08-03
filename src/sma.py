import matplotlib.pyplot as plt
import time


def compute_sma(df, window=50):
    """
    Calculate and plot the SMA for visualization.
    """
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    plt.plot(df['Date'], df[f'SMA_{window}'], label=f'SMA {window}')
    plt.legend()
    plt.title(f'Simple Moving Average ({window}-day)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/sma_plot.png')
    plt.close()


def sma_signal(df, window=50):
    """
    Compute the current price vs. SMA signal for the last date.
    """
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    current_price = df['Close'].iloc[-1]
    current_sma = df[f'SMA_{window}'].iloc[-1]
    signal = "BUY (Price > SMA)" if current_price > current_sma else "SELL (Price < SMA)"
    return {
        "current": current_price,
        "sma": current_sma,
        "signal": signal
    }


def evaluate_sma(df, window=50):
    """
    Evaluate SMA strategy over the entire series:
      - Accuracy: % correct directional predictions
      - ROI: simulated profit % by taking long positions when signal = BUY
      - Duration: execution time in seconds
    """
    start = time.time()
    data = df.copy()
    data[f'SMA'] = data['Close'].rolling(window=window).mean()
    data = data.dropna().reset_index(drop=True)
    # signals: True if price > SMA
    signals = data['Close'] > data['SMA']
    prices = data['Close']
    next_prices = prices.shift(-1)
    valid = next_prices.notna()
    signals = signals[valid]
    prices = prices[valid]
    next_prices = next_prices[valid]
    actual_up = next_prices > prices
    accuracy = (signals == actual_up).mean() * 100
    # simulated profit: sum of (next - current) when signal is True
    profit = (next_prices - prices)[signals].sum()
    # ROI as percent of capital deployed: assume $1 per BUY
    trades = prices[signals]
    roi = (profit / trades.sum()) * 100 if trades.sum() else 0.0
    duration = time.time() - start
    return {"accuracy": accuracy, "roi": roi, "duration": duration}
