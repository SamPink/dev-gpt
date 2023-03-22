import pandas as pd
import yfinance as yf
from fbprophet import Prophet

# Fetching TESLA historical data
symbol = "TSLA"
start_date = "2022-01-01"
end_date = "2022-12-31"
data = yf.download(symbol, start=start_date, end=end_date)
data.reset_index(inplace=True)

# Preparing data for Prophet model
data = data[["Date", "Close"]]
data.columns = ["ds", "y"]

# Create and fit the Prophet model
model = Prophet(daily_seasonality=True)
model.fit(data)

# Predicting TESLA price for the next 30 days
future = model.make_future_dataframe(periods=30)
forecast = model.predict(future)

# Filter the predictions for the next 30 days
next_30_days = forecast.tail(30)[["ds", "yhat", "yhat_lower", "yhat_upper"]]
print(next_30_days)