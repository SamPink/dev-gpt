import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

def get_eth_historical_price(days=30):
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    start_date_str = start_date.strftime('%d-%m-%Y')
    end_date_str = end_date.strftime('%d-%m-%Y')
    
    url = f'https://api.coingecko.com/api/v3/coins/ethereum/market_chart/range?vs_currency=gbp&from={start_date.timestamp()}&to={end_date.timestamp()}'
    response = requests.get(url)
    
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        return None

def plot_eth_price(data):
    df = pd.DataFrame(data['prices'], columns=['timestamp', 'price'])
    df['date'] = pd.to_datetime(df['timestamp'], unit='ms')
    df.set_index('date', inplace=True)

    plt.plot(df.index, df['price'])
    plt.xlabel('Date')
    plt.ylabel('Price (GBP)')
    plt.title('Ethereum Price in GBP for the Last 30 Days')
    plt.xticks(rotation=45)
    plt.grid()
    plt.show()

historical_data = get_eth_historical_price(days=30)
if historical_data is not None:
    plot_eth_price(historical_data)
else:
    print("Unable to fetch historical data.")