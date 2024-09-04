import csv
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="mysqluser",
    password="secret1234",
    database="forecast_db"
)
cursor = db.cursor()

with open('.csv', 'r') as file:
    reader = csv.reader(file)

    for row in reader:
        column1 = row[0]
        column2 = row[1]
        query = "INSERT INTO table (column1, column2) VALUES (%s, %s)"
        cursor.execute(query, (column1, column2))

db.commit()
cursor.close()
db.close()