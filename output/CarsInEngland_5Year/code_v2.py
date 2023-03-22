import matplotlib.pyplot as plt
import statistics 

def main():
    years = [2016, 2017, 2018, 2019, 2020]
    number_of_cars = [31.7e6, 32.3e6, 32.5e6, 32.2e6, 31.9e6]
    avg_car_prices = [14500, 14625, 14700, 14830, 15020]

    avg_car_price = statistics.mean(avg_car_prices)

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

    plt.title(f'Number of Cars and Average Price in England (2016 - 2020)\nMean Price: £{avg_car_price}')
    fig.tight_layout()
    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()