from helper import load_stock_data
from sma import compute_sma
from linear_regression import train_and_predict

def main():
    symbol = "AAPL"
    df = load_stock_data(symbol)
    compute_sma(df)
    train_and_predict(df)

if __name__ == "__main__":
    main()