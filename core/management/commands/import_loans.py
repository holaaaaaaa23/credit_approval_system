import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Loan, Customer
from datetime import datetime

class Command(BaseCommand):
    help = 'Import loan data from Excel'

    def handle(self, *args, **kwargs):
        df = pd.read_excel('loan_data.xlsx')

        for index, row in df.iterrows():
            loan_id = row['Loan ID']
            if Loan.objects.filter(id=loan_id).exists():
                print(f"⏩ Loan ID {loan_id} already exists, skipping...")
                continue

            customer_id = row['Customer ID']
            try:
                customer = Customer.objects.get(id=customer_id)
            except Customer.DoesNotExist:
                print(f"❌ Customer ID {customer_id} not found, skipping loan ID {loan_id}")
                continue

            Loan.objects.create(
                id=loan_id,
                customer=customer,
                loan_amount=row['Loan Amount'],
                interest_rate=row['Interest Rate'],
                tenure=row['Tenure'],
                monthly_installment=row['Monthly repayment (EMI)'],
                emi_paid_on_time=row['EMIs paid on time'],
                start_date=datetime.strptime(str(row['Start Date']), "%Y-%m-%d"),
                end_date=datetime.strptime(str(row['End Date']), "%Y-%m-%d"),
                loan_approved=True  # since it's past data
            )
            print(f"✅ Imported Loan ID {loan_id} for Customer ID {customer_id}")
