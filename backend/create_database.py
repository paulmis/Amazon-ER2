import csv
import sqlite3

# Function to create the SQLite table
def create_table():
    connection = sqlite3.connect('aws.db')
    cursor = connection.cursor()

    # Define the table schema
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS product (
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
            Product_Name TEXT,
            Brand_Name TEXT,
            Price REAL,
            Rating INTEGER,
            Reviews TEXT,
            Review_Votes INTEGER
        )
    ''')

    # Create search index on Product_Name
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_product_name ON product (Product_Name)
    ''')

    # Create search index on Brand_Name
    cursor.execute('''
        CREATE INDEX IF NOT EXISTS idx_brand_name ON product (Brand_Name)
    ''')

    connection.commit()
    connection.close()

# Function to insert data into the SQLite table
def insert_data(data):
    connection = sqlite3.connect('aws.db')
    cursor = connection.cursor()

    # Insert data into the table
    cursor.executemany('''
        INSERT INTO product (Product_Name, Brand_Name, Price, Rating, Reviews, Review_Votes)
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

    return data

if __name__ == "__main__":
    # Specify the CSV file path
    csv_filename = '/home/yigit/Downloads/archive/Amazon_Unlocked_Mobile.csv'

    # Create the table in the SQLite database
    create_table()

    # Read data from the CSV file
    csv_data = read_csv(csv_filename)

    # Insert data into the SQLite database
    insert_data(csv_data)
