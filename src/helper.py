import yfinance as yf
import pandas as pd

def load_stock_data(symbol, start="2022-01-01", end="2025-01-01"):
    df = yf.download(symbol, start=start, end=end, auto_adjust=True)
    df = df[["Close"]]
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return df
