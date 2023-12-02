import csv
import sqlite3

CSV_FILE =  'ai/data/preprocessed_dataset_b2a8b513791b1ec82721131a232a4be720297cdf3147009738cb15abd88ad51e.csv'
SQLITE_DB = 'instance/aws.db'

# Function to insert data into the SQLite table
def insert_data(data):
    connection = sqlite3.connect(SQLITE_DB)
    cursor = connection.cursor()

    # Insert data into the table
    cursor.executemany('''
        INSERT INTO comment (product, brand, price, rating, review, votes)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', data)

    connection.commit()
    connection.close()

# Function to read data from the CSV file
def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        data = [row for row in reader]

    # Remove last column
    for row in data:
        del row[-1]
    return data

if __name__ == "__main__":
    # Specify the CSV file path
    csv_filename = CSV_FILE

    # Read data from the CSV file
    csv_data = read_csv(csv_filename)

    # Insert data into the SQLite database
    insert_data(csv_data)
