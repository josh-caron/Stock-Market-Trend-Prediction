import yfinance as yf

def load_stock_data(symbol, start="2015-01-01", end=None):
    df = yf.download(symbol, start=start, end=end)
    df.reset_index(inplace=True)
    # Only keep the columns we need
    return [{"Date": row["Date"], "Close": float(row["Close"])} for _, row in df.iterrows()]
