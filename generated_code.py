Here's a simple Python script to read a CSV file and print its contents using the `csv` module:

```python
import csv

# Replace the filename below with the path to your CSV file
csv_file_path = 'path/to/your/csvfile.csv'

# Open the file in read mode and read its contents using csv.reader
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)

    # Iterate through each row in the CSV file
    for row in csv_reader:
        # Print the entire row
        print(row)
```

Make sure to update the `csv_file_path` variable with the actual path to your CSV file. This script will read the CSV file and print each row as a list of values.