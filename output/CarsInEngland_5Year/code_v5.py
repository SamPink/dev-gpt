import matplotlib.pyplot as plt
import pandas as pd

def main():
    # Read the data from the CSV file
    df = pd.read_csv('veh0101.csv')

    # Filter the data to keep only England and car vehicles
    df = df[(df['area_name'] == 'england') & (df['vehicle_type'] == 'Cars')]

    # Extract the years and the total number of vehicles
    years = df['year'].tolist()
    number_of_cars = df['total_licensed'].tolist()

    # Plot the data
    plt.plot(years, number_of_cars, marker='o')
    plt.xlabel('Years')
    plt.ylabel('Number of Cars (in millions)')
    plt.title('Number of Cars in England')

    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()