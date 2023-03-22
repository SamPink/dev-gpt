import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
import requests
from odf.opendocument import load
from odf import table, text

def read_ods(url):
    response = requests.get(url)
    ods_file = load(BytesIO(response.content))

    data = []
    sheet = ods_file.spreadsheet.getElementsByType(table.Table)[0]

    for row in sheet.getElementsByType(table.TableRow)[1:]:
        cells = row.getElementsByType(table.TableCell)
        data.append([text.textextract(cell) for cell in cells])

    return pd.DataFrame(data)

def main():
    url = "https://assets.publishing.service.gov.uk/government/uploads/system/uploads/attachment_data/file/1034200/veh0101.ods"
    df = read_ods(url)

    df.columns = ['year', 'area_code', 'area_name', 'vehicle_type', 'total_licensed', 'total_unlicensed', 'total_all']
    df[['year', 'total_licensed']] = df[['year', 'total_licensed']].apply(pd.to_numeric)

    df = df[(df['area_name'] == 'england') & (df['vehicle_type'] == 'Cars')]

    years = df['year'].tolist()
    number_of_cars = df['total_licensed'].tolist()

    plt.plot(years, number_of_cars, marker='o')
    plt.xlabel('Years')
    plt.ylabel('Number of Cars (in millions)')
    plt.title('Number of Cars in England')

    plt.grid()
    plt.show()

if __name__ == '__main__':
    main()