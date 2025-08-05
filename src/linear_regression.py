def fit_linear_regression(x, y):
    # Least squares: y = m*x + b
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n
    num = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    den = sum((x[i] - mean_x) ** 2 for i in range(n))
    m = num / den if den != 0 else 0.0
    b = mean_y - m * mean_x
    return m, b

def train_and_predict(data):
    import matplotlib.pyplot as plt
    import os
    os.makedirs('plots', exist_ok=True)
    # Predict close[t+1] from close[t]
    prices = [row["Close"] for row in data]
    prev = prices[:-1]
    curr = prices[1:]
    if len(prev) < 2:
        print("Not enough data for regression!")
        return
    m, b = fit_linear_regression(prev, curr)
    preds = [m * x + b for x in prev]
    dates = [row["Date"] for row in data][1:]
    plt.figure(figsize=(12, 6))
    plt.plot(dates, curr, label="Actual")
    plt.plot(dates, preds, label="Predicted", linestyle="--", color="green")
    plt.legend()
    plt.title("Linear Regression Prediction")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("plots/lr_plot.png")
    plt.show()
    plt.close()

def regression_signal(data):
    prices = [row["Close"] for row in data]
    if len(prices) < 3:
        return {"predicted": None, "current": None, "signal": "Not enough data for regression", "slope": None, "intercept": None}
    prev = prices[:-1]
    curr = prices[1:]
    m, b = fit_linear_regression(prev, curr)
    predicted = m * prices[-2] + b
    current = prices[-1]
    signal = "BUY (Predicted > Current)" if predicted > current else "SELL (Predicted < Current)"
    return {"predicted": predicted, "current": current, "signal": signal, "slope": m, "intercept": b}

def evaluate_regression(data):
    import time
    start = time.time()
    prices = [row["Close"] for row in data]
    if len(prices) < 3:
        return {"accuracy": 0.0, "duration": 0.0}
    prev = prices[:-1]
    curr = prices[1:]
    m, b = fit_linear_regression(prev, curr)
    preds = [m * x + b for x in prev]
    acc_count = 0
    total = 0
    for i in range(len(preds)-1):
        signal = preds[i] > prev[i]
        actual_up = curr[i+1] > prev[i+1]
        acc_count += signal == actual_up
        total += 1
    accuracy = (acc_count / total) * 100 if total > 0 else 0.0
    duration = time.time() - start
    return {"accuracy": accuracy, "duration": duration}
