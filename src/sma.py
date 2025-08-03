import matplotlib.pyplot as plt

def compute_sma(df, window_sizes=[10, 50]):
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