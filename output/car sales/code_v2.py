import requests
from bs4 import BeautifulSoup

def get_top_cars(year):
    url = f"https://en.wikipedia.org/wiki/List_of_bestselling_vehicles_in_the_United_States"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    tables = soup.find_all("table", class_="wikitable")
    top_cars = []

    for table in tables:
        caption = table.find("caption")
        if caption and caption.text.strip().startswith(f"Best-selling vehicles in {year} in United States"):
            rows = table.find_all("tr")
            for i, row in enumerate(rows[1:]):
                data = row.find_all("td")
                rank, make_model = data[0].text.strip(), data[1].text.strip()
                top_cars.append((rank, make_model))
                if i >= 9:  # gets the top 10 cars
                    break
            break

    return top_cars

if __name__ == "__main__":
    year = 2019
    top_cars = get_top_cars(year)

    print(f"Top 10 cars sold in the US in {year}:")
    for rank, make_model in top_cars:
        print(f"{rank}. {make_model}")