import yfinance as yf
import pandas as pd

def load_stock_data(symbol, start="2015-01-01", end=None):
    df = yf.download(symbol, start=start, end=end)
    df = df[["Close"]]
    df.dropna(inplace=True)
    df.reset_index(inplace=True)
    return df
