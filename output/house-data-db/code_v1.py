import sqlite3

def main():
    database_file = "sqlite:///uk_properties.db"

    connection = sqlite3.connect(database_file)
    cursor = connection.cursor()

    top_10_expensive_properties_query = """
        SELECT * FROM properties
        WHERE TownCity = 'London'
        ORDER BY Price DESC
        LIMIT 10;
    """

    cursor.execute(top_10_expensive_properties_query)

    results = cursor.fetchall()
    
    for row in results:
        print(row)

    cursor.close()
    connection.close()


if __name__ == "__main__":
    main()