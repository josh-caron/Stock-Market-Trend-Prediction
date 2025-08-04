import time
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def train_and_predict(df):
    import os
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
    plt.figure(figsize=(12, 6))
    plt.plot(data['Date'][split:], y_test, label='Actual', color='royalblue')
    plt.plot(data['Date'][split:], preds, label='Predicted', color='orange', linewidth=2)
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
    from sklearn.linear_model import LinearRegression
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
    import time
    import numpy as np
    from sklearn.linear_model import LinearRegression

    start = time.time()
    data = df[['Close']].copy().reset_index(drop=True)

    if len(data) < 3:
        return {"accuracy": 0.0, "duration": 0.0}

    X = np.arange(len(data) - 1).reshape(-1, 1)
    y = data['Close'].values[:-1]

    model = LinearRegression()
    model.fit(X, y)
    preds = model.predict(X)

    actuals = data['Close'].values[1:]
    signals = preds < y
    actual_up = actuals > y

    accuracy = (signals == actual_up).mean() * 100
    duration = time.time() - start
    return {"accuracy": accuracy, "duration": duration}


