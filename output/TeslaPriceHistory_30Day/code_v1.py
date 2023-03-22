import pandas as pd
import pandas_datareader as pdr
import datetime as dt
import matplotlib.pyplot as plt

# Set the end date to today and start date to 30 days ago
end_date = dt.date.today()
start_date = end_date - dt.timedelta(days=30)

# Fetch Tesla's stock data
ticker = "TSLA"
stock_data = pdr.get_data_yahoo(ticker, start_date, end_date)

# Plot the stock data
plt.figure(figsize=(12,6))
plt.plot(stock_data.index, stock_data["Close"], label=ticker)
plt.xlabel("Date")
plt.ylabel("Close Price")
plt.title(f"{ticker} Stock Price History (Last 30 days)")
plt.legend()
plt.show()