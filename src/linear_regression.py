from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np
import matplotlib.pyplot as plt

def train_and_predict(df):
    df['Prev_Close'] = df['Close'].shift(1)
    df.dropna(inplace=True)

    X = df[['Prev_Close']].values
    y = df['Close'].values

    split = int(0.8 * len(df))
    X_train, X_test = X[:split], X[split:]
    y_train, y_test = y[:split], y[split:]

    model = LinearRegression()
    model.fit(X_train, y_train)
    predictions = model.predict(X_test)

    mse = mean_squared_error(y_test, predictions)
    print(f'Mean Squared Error: {mse:.4f}')

    plt.figure(figsize=(12, 6))
    plt.plot(df['Date'][split:], y_test, label='Actual')
    plt.plot(df['Date'][split:], predictions, label='Predicted')
    plt.legend()
    plt.title('Linear Regression Prediction')
    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig('plots/lr_plot.png')
    plt.close()

def regression_signal(df):
    df['Prev_Close'] = df['Close'].shift(1)
    df.dropna(inplace=True)

    X = df[['Prev_Close']].values
    y = df['Close'].values

    model = LinearRegression()
    model.fit(X, y)
    predicted_price = model.predict([[df['Close'].iloc[-1]]])[0]
    current_price = df['Close'].iloc[-1]
    signal = "BUY (Predicted > Current)" if predicted_price > current_price else "SELL (Predicted < Current)"
    return {
        "predicted": predicted_price,
        "current": current_price,
        "signal": signal,
        "slope": model.coef_[0],
        "intercept": model.intercept_
    }
