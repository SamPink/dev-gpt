import yfinance as yf
import matplotlib.pyplot as plt
import mplfinance as mpf
import pandas as pd

# Fetch stock market data
def get_stock_data(ticker, start, end):
    stock_data = yf.download(ticker, start=start, end=end)
    return stock_data

# Plot stock market data
def plot_stock_data(stock_data, ticker):
    mpf.plot(stock_data, type='candle', title=f'{ticker} Price', ylabel='Price (USD)', style='yahoo', volume=True, tight_layout=True)
    plt.show()

# Get and plot Microsoft stock data
ticker = 'MSFT'
start = '2020-01-01'
end = '2022-01-01'
stock_data = get_stock_data(ticker, start, end)
plot_stock_data(stock_data, ticker)