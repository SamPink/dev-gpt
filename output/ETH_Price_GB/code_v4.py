import requests
import pandas as pd
import matplotlib.pyplot as plt
from fbprophet import Prophet
from datetime import datetime, timedelta

def get_crypto_prices_for_past_2_years(crypto_id):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365*2)
    start_timestamp = int(start_date.timestamp())
    end_timestamp = int(end_date.timestamp())
    
    url = f"https://api.coingecko.com/api/v3/coins/{crypto_id}/market_chart/range?vs_currency=gbp&from={start_timestamp}&to={end_timestamp}"

    response = requests.get(url)
    data = response.json()
    
    crypto_prices_gbp = [price_point[1] for price_point in data["prices"]]
    timestamp_dates = [price_point[0] for price_point in data["prices"]]
    
    return timestamp_dates, crypto_prices_gbp

def make_prophet_prediction(timestamp_dates, crypto_prices_gbp, days_to_predict):
    dates = [datetime.fromtimestamp(ts // 1000) for ts in timestamp_dates]

    data = {
        "ds": dates,
        "y": crypto_prices_gbp
    }
    df = pd.DataFrame(data)

    model = Prophet()
    model.fit(df)

    future = model.make_future_dataframe(periods=days_to_predict)
    forecast = model.predict(future)

    return forecast

def plot_prophet_forecast(forecast, crypto_name):
    fig = model.plot(forecast, xlabel="Date", ylabel=f"{crypto_name} Price in GBP")
    plt.title(f"{crypto_name} Price Prediction for the Next 30 Days")
    plt.grid()
    plt.tight_layout()
    plt.show()

days_to_predict = 30

timestamp_dates, eth_prices_gbp = get_crypto_prices_for_past_2_years("ethereum")
eth_forecast = make_prophet_prediction(timestamp_dates, eth_prices_gbp, days_to_predict)
plot_prophet_forecast(eth_forecast, "Ethereum (ETH)")

timestamp_dates, btc_prices_gbp = get_crypto_prices_for_past_2_years("bitcoin")
btc_forecast = make_prophet_prediction(timestamp_dates, btc_prices_gbp, days_to_predict)
plot_prophet_forecast(btc_forecast, "Bitcoin (BTC)")