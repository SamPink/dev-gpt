import matplotlib.pyplot as plt

def main():
    years = [2016, 2017, 2018, 2019, 2020]
    number_of_cars = [31.7e6, 32.3e6, 32.5e6, 32.2e6, 31.9e6]

    plt.plot(years, number_of_cars, marker='o')
    plt.xlabel('Years')
    plt.xticks(years)
    plt.ylabel('Number of Cars (in millions)')
    plt.title('Number of Cars in England over the Last 5 Years')

    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()