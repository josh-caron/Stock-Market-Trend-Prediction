def compute_sma_manual(prices, window):
    sma = []
    for i in range(len(prices)):
        if i < window - 1:
            sma.append(None)
        else:
            avg = sum(prices[i-window+1:i+1]) / window
            sma.append(avg)
    return sma

def compute_sma(data, window=50):
    # For plotting
    import matplotlib.pyplot as plt
    import os
    os.makedirs('plots', exist_ok=True)
    dates = [row["Date"] for row in data]
    prices = [row["Close"] for row in data]
    sma = compute_sma_manual(prices, window)
    plt.figure(figsize=(12, 6))
    plt.plot(dates, prices, label="Close Price", color="royalblue")
    plt.plot(dates, [v if v is not None else float('nan') for v in sma], label=f"SMA {window}", color="red", linewidth=2.5)
    plt.legend()
    plt.title(f'Simple Moving Average ({window}-day)')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/sma_plot.png')
    plt.show()
    plt.close()

def sma_signal(data, window=50):
    prices = [row["Close"] for row in data]
    sma = compute_sma_manual(prices, window)
    if sma[-1] is None:
        return {"current": prices[-1], "sma": None, "signal": "Not enough data for SMA"}
    else:
        signal = "BUY (Price > SMA)" if prices[-1] > sma[-1] else "SELL (Price < SMA)"
        return {"current": prices[-1], "sma": sma[-1], "signal": signal}

def evaluate_sma(data, window=50):
    import time
    start = time.time()
    prices = [row["Close"] for row in data]
    sma = compute_sma_manual(prices, window)
    # Remove entries without valid SMA
    valid_indices = [i for i, val in enumerate(sma) if val is not None]
    if len(valid_indices) < 2:
        return {"accuracy": 0.0, "duration": 0.0}
    acc_count = 0
    total = 0
    for idx in valid_indices[:-1]:
        signal = prices[idx] > sma[idx]
        actual_up = prices[idx+1] > prices[idx]
        acc_count += signal == actual_up
        total += 1
    accuracy = (acc_count / total) * 100 if total > 0 else 0.0
    duration = time.time() - start
    return {"accuracy": accuracy, "duration": duration}
