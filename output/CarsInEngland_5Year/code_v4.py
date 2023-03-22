import matplotlib.pyplot as plt
import requests

def get_number_of_cars(year):
    url = f"https://data.gov.uk/api/3/action/datastore_search?resource_id=1899ecf1-bd0d-4130-8cc2-da40e33f649f&q={{%22year%22:%22{year}%22,%22area%22:%22england%22}}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        total_cars = data['result']['records'][0]['total_licensed']
        return total_cars
    else:
        print(f"Error fetching number of cars for {year}: {response.status_code}")
        return None

def get_average_car_prices():
    # Replace this function with a call to an API that provides average car prices for England (if available)
    # Currently, there are no known public APIs providing this information
    return [14500, 14625, 14700, 14830, 15020]

def main():
    years = [2016, 2017, 2018, 2019, 2020]
    number_of_cars = [get_number_of_cars(year) for year in years]
    avg_car_prices = get_average_car_prices()

    fig, ax1 = plt.subplots()

    color = 'tab:blue'
    ax1.set_xlabel('Years')
    ax1.set_xticks(years)
    ax1.set_ylabel('Number of Cars (in millions)', color=color)
    ax1.plot(years, number_of_cars, marker='o', color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()

    color = 'tab:red'
    ax2.set_ylabel('Average Car Price (£)', color=color)
    ax2.plot(years, avg_car_prices, marker='o', color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title(f'Number of Cars and Average Price in England (2016 - 2020)')
    fig.tight_layout()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()