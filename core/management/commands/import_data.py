from django.core.management.base import BaseCommand
from core.models import Customer, Loan
import pandas as pd

class Command(BaseCommand):
    help = 'Import customer and loan data from Excel files'

    def handle(self, *args, **kwargs):
        # === 1. Import Customers ===
        df_customers = pd.read_excel('customer_data.xlsx')
        df_customers.columns = df_customers.columns.str.strip()

        for _, row in df_customers.iterrows():
            Customer.objects.update_or_create(
                id=row['Customer ID'],
                defaults={
                    'first_name': row['First Name'],
                    'last_name': row['Last Name'],
                    'phone_number': str(row['Phone Number']),
                    'monthly_salary': row['Monthly Salary'],
                    'approved_limit': row['Approved Limit'],
                    'current_debt': 0.0,  # default since not in sheet
                    'age': row['Age']
                }
            )

        # === 2. Import Loans ===
        df_loans = pd.read_excel('loan_data.xlsx')
        df_loans.columns = df_loans.columns.str.strip()

        for _, row in df_loans.iterrows():
            try:
                customer = Customer.objects.get(id=row['Customer ID'])
                Loan.objects.update_or_create(
                    id=row['Loan ID'],
                    defaults={
                        'customer': customer,
                        'loan_amount': row['Loan Amount'],
                        'tenure': row['Tenure'],
                        'interest_rate': row['Interest Rate'],
                        'monthly_installment': row['Monthly payment'],
                        'emis_paid_on_time': row['EMIs paid on Time'],
                        'start_date': pd.to_datetime(row['Date of Approval']),
                        'end_date': pd.to_datetime(row['End Date'])
                    }
                )
            except Customer.DoesNotExist:
                self.stdout.write(f"⚠️ Customer ID {row['Customer ID']} not found — skipping loan.")

        self.stdout.write(self.style.SUCCESS('✅ Customer and loan data imported successfully!'))
