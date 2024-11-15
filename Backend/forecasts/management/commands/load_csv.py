import csv
import mysql.connector
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Upload CSV data to dynamically created tables for each economic indicator'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')
        parser.add_argument('indicator', type=str, help='Name of the economic indicator (e.g., gdp, unemployment, etc.)')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        indicator_name = options['indicator'].lower()  # Ensure lowercase for table names

        # Connect to the MySQL database
        db = mysql.connector.connect(
            host="localhost",
            user="mysqluser",
            password="secret1234",
            database="forecast_db"
        )
        cursor = db.cursor()

        try:
            # Open the CSV file
            with open(csv_file_path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                headers = reader.fieldnames  # Get the CSV file headers
                print("CSV Headers:", headers)  # Debugging line to check headers

                # Dynamically create a SQL CREATE TABLE statement
                create_table_query = f"CREATE TABLE IF NOT EXISTS {indicator_name} (id INT AUTO_INCREMENT PRIMARY KEY, "
                create_table_query += ", ".join([f"`{header}` VARCHAR(255)" for header in headers])  # Use backticks
                create_table_query += ");"
                
                # Execute the CREATE TABLE query
                cursor.execute(create_table_query)
                db.commit()

                # Insert data from CSV into the newly created table
                insert_query = f"INSERT INTO {indicator_name} ({', '.join([f'`{header}`' for header in headers])}) VALUES ({', '.join(['%s' for _ in headers])})"
                
                # Read and insert each row of the CSV file
                for row in reader:
                    cursor.execute(insert_query, [row[header] for header in headers])

                db.commit()
                self.stdout.write(self.style.SUCCESS(f'Successfully uploaded data to the {indicator_name} table'))
        
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error: {str(e)}'))
        
        finally:
            cursor.close()
            db.close()
