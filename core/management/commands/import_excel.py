import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Customer

class Command(BaseCommand):
    help = 'Import customer data from Excel'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('customer_data.xlsx')

        for index, row in df.iterrows():
            customer_id = row['Customer ID']
            if Customer.objects.filter(id=customer_id).exists():
                print(f"⏩ Customer ID {customer_id} already exists, skipping...")
                continue

            Customer.objects.create(
                id=customer_id,
                first_name=row['First Name'],
                last_name=row['Last Name'],
                age=row['Age'],
                phone_number=str(row['Phone Number']),
                monthly_salary=row['Monthly Salary'],
                approved_limit=row['Approved Limit'],
                current_debt=0  # Or read from sheet if available
            )
            print(f"✅ Imported: {row['First Name']} {row['Last Name']} (ID: {customer_id})")
