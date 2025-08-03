import matplotlib.pyplot as plt

def compute_sma(df, window_sizes=[50]):
    for window in window_sizes:
        df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()

    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'], df['Close'], label='Close Price')
    for window in window_sizes:
        plt.plot(df['Date'], df[f'SMA_{window}'], label=f'SMA {window}')
    plt.legend()
    plt.title('Simple Moving Averages')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/sma_plot.png')
    plt.close()

def sma_signal(df, window=50):
    df[f'SMA_{window}'] = df['Close'].rolling(window=window).mean()
    current_price = df['Close'].iloc[-1]
    current_sma = df[f'SMA_{window}'].iloc[-1]
    signal = "BUY (Price > SMA)" if current_price > current_sma else "SELL (Price < SMA)"
    return {
        "current": current_price,
        "sma": current_sma,
        "signal": signal
    }