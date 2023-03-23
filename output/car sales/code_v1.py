import requests
from bs4 import BeautifulSoup

def get_top_cars(year):
    url = f"https://www.goodcarbadcar.net/{year}-year-end-us-vehicle-sales-rankings-top-296-best-selling-vehicles-in-america/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table")
    rows = table.find_all("tr")
    top_cars = []

    for i, row in enumerate(rows[1:]):
        data = row.find_all("td")
        rank, make_model, sales = data[0].text, data[1].text, data[2].text
        top_cars.append((rank, make_model, sales))
        if i >= 9:  # gets the top 10 cars
            break

    return top_cars

if __name__ == "__main__":
    year = 2019
    top_cars = get_top_cars(year)

    print(f"Top 10 cars sold in the US in {year}:")
    for rank, make_model, sales in top_cars:
        print(f"{rank}. {make_model} - {sales}")