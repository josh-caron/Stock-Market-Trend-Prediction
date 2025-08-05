def plot_combined(data, window=50):
    import matplotlib.pyplot as plt
    # Compute SMA
    prices = [row["Close"] for row in data]
    dates = [row["Date"] for row in data]
    sma = []
    for i in range(len(prices)):
        if i < window - 1:
            sma.append(None)
        else:
            avg = sum(prices[i-window+1:i+1]) / window
            sma.append(avg)
    # Linear regression prediction
    if len(prices) < 3:
        print("Not enough data for regression to show combined graph!")
        return
    prev = prices[:-1]
    curr = prices[1:]
    m, b = fit_linear_regression(prev, curr)
    preds = [None] + [m * x + b for x in prev]  # shift by 1
    plt.figure(figsize=(12, 6))
    plt.plot(dates, prices, label="Close Price", color="royalblue", linewidth=1)
    plt.plot(dates, [v if v is not None else float('nan') for v in sma], label=f"SMA {window}", color="red", linewidth=2.5)
    plt.plot(dates, [v if v is not None else float('nan') for v in preds], label="LR Predicted", color="green", linestyle='--', linewidth=2)
    plt.legend()
    plt.title('Actual vs SMA vs Linear Regression')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
    plt.close()

def fit_linear_regression(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den = sum((x[i] - mean_x) ** 2 for i in range(n))
    m = num / den if den != 0 else 0.0
    b = mean_y - m * mean_x
    return m, b
