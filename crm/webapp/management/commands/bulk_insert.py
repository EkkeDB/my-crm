import os
import pandas as pd
from django.core.management.base import BaseCommand
from webapp.models import Trader  # Replace with your actual model

class Command(BaseCommand):
    help = 'Bulk insert rows into the PostgreSQL database from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the CSV file')

    def handle(self, *args, **kwargs):
        file_path = 'static/assets/trader.csv'  # Specify the path to your CSV file

        # Construct the absolute path to the CSV file
        full_path = os.path.abspath(file_path)

        # Read data from the CSV file using pandas
        try:
            df = pd.read_csv(full_path, delimiter=';')
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f"File '{full_path}' not found."))
            return
        except pd.errors.EmptyDataError:
            self.stdout.write(self.style.ERROR(f"File '{full_path}' is empty."))
            return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error reading file '{full_path}': {e}"))
            return

        # Convert the dataframe to a list of dictionaries
        data_to_insert = df.to_dict(orient='records')

        # Bulk insert data into the PostgreSQL database using Django ORM
        try:
            Trader.objects.bulk_create([Trader(id_trader=row['id_trader'], trader_name=row['trader_name']) for row in data_to_insert])
            self.stdout.write(self.style.SUCCESS('Successfully inserted data'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error inserting data: {e}"))
